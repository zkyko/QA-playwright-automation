"""
Jira/Zephyr Scale Integration Utility
Handles test cycle creation, test execution updates, and defect creation
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class JiraZephyrIntegration:
    """Integration class for Jira and Zephyr Scale API interactions"""
    
    def __init__(self):
        self.base_url = os.getenv('JIRA_BASE_URL')
        self.email = os.getenv('JIRA_EMAIL')
        self.api_token = os.getenv('JIRA_API_TOKEN', 'ATATT3xFfGF0BxUlEOAQG-AWfFM1_93IEf8OKMIPgxBDPzlTeR5MmPAnOg_7unFzVOW7MsGukdrpbWw05eouwbYDtyIp2SWCpnQPjeZqU4CqzXk25tHv0T6RUouvZoK3-oBmfjO-3lGm5QD7omsEeCDx2X0gdLT9gDqn1i34TVWaVaGo=C852BE5A')
        self.project_key = os.getenv('JIRA_PROJECT_KEY')
        
        # Zephyr Scale Cloud API endpoints
        self.zephyr_api_base = "https://api.zephyrscale.smartbear.com/v2"
        
        self.session = requests.Session()
        self.session.auth = (self.email, self.api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        # Zephyr Scale uses bearer token auth
        self.zephyr_session = requests.Session()
        self.zephyr_session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_token}'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request to Jira API with error handling"""
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            raise
    
    def create_test_cycle(self, name: str, project_key: str, version: Optional[str] = None) -> str:
        """
        Create a new test cycle in Zephyr Scale Cloud
        
        Args:
            name: Name of the test cycle
            project_key: Jira project key
            version: Optional version/release name
            
        Returns:
            Test cycle key
        """
        print(f"Creating test cycle: {name}")
        
        # Zephyr Scale Cloud API v2
        url = f"{self.zephyr_api_base}/testcycles"
        
        payload = {
            "name": name,
            "projectKey": project_key,
        }
        
        if version:
            payload["jiraProjectVersion"] = version
        
        try:
            response = self.zephyr_session.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            cycle_key = data.get('key')
            
            # Save cycle key to file for use in subsequent jobs
            with open('test_cycle_key.txt', 'w') as f:
                f.write(cycle_key)
            
            print(f"✓ Test cycle created: {cycle_key}")
            print(f"  URL: {self.base_url}/projects/{project_key}/testcycle/{cycle_key}")
            
            return cycle_key
        except Exception as e:
            print(f"✗ Failed to create test cycle: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"  Response: {e.response.text}")
            # Create a fallback identifier
            fallback_key = f"MANUAL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            with open('test_cycle_key.txt', 'w') as f:
                f.write(fallback_key)
            return fallback_key
    
    def parse_junit_results(self, junit_file: str) -> List[Dict]:
        """
        Parse JUnit XML results file
        
        Args:
            junit_file: Path to JUnit XML file
            
        Returns:
            List of test results
        """
        tree = ET.parse(junit_file)
        root = tree.getroot()
        
        results = []
        
        for testsuite in root.findall('.//testsuite'):
            for testcase in testsuite.findall('.//testcase'):
                test_name = testcase.get('name')
                classname = testcase.get('classname')
                time = float(testcase.get('time', 0))
                
                # Determine test status
                failure = testcase.find('failure')
                error = testcase.find('error')
                skipped = testcase.find('skipped')
                
                if failure is not None:
                    status = 'FAIL'
                    message = failure.get('message', '')
                elif error is not None:
                    status = 'FAIL'
                    message = error.get('message', '')
                elif skipped is not None:
                    status = 'BLOCKED'
                    message = 'Test skipped'
                else:
                    status = 'PASS'
                    message = ''
                
                # Try to extract Jira test case key from test name or docstring
                # Expected format: test_name (TEST-123) or @pytest.mark.jira('TEST-123')
                jira_key = self._extract_jira_key(test_name, classname)
                
                results.append({
                    'test_name': test_name,
                    'classname': classname,
                    'status': status,
                    'duration': time,
                    'message': message,
                    'jira_key': jira_key
                })
        
        return results
    
    def _extract_jira_key(self, test_name: str, classname: str) -> Optional[str]:
        """Extract Jira test case key from test metadata"""
        import re
        
        # Look for pattern like TEST-123, PROJ-456, etc.
        pattern = r'([A-Z]+-\d+)'
        
        # Check test name
        match = re.search(pattern, test_name)
        if match:
            return match.group(1)
        
        # Check classname
        match = re.search(pattern, classname)
        if match:
            return match.group(1)
        
        return None
    
    def update_test_results(self, cycle_key: str, junit_file: str, test_type: str = ""):
        """
        Update test execution results in Jira/Zephyr
        
        Args:
            cycle_key: Test cycle key
            junit_file: Path to JUnit XML results file
            test_type: Type of tests (e.g., smoke, e2e)
        """
        print(f"\nUpdating test results for cycle: {cycle_key}")
        print(f"  Test type: {test_type}")
        print(f"  Results file: {junit_file}")
        
        if not os.path.exists(junit_file):
            print(f"✗ Results file not found: {junit_file}")
            return
        
        results = self.parse_junit_results(junit_file)
        
        print(f"\nProcessing {len(results)} test results...")
        
        success_count = 0
        fail_count = 0
        skip_count = 0
        
        for result in results:
            status = result['status']
            test_name = result['test_name']
            jira_key = result['jira_key']
            
            if status == 'PASS':
                success_count += 1
            elif status == 'FAIL':
                fail_count += 1
            else:
                skip_count += 1
            
            # If test has associated Jira key, update it
            if jira_key:
                self._update_test_execution(
                    cycle_key=cycle_key,
                    test_key=jira_key,
                    status=status,
                    duration=result['duration'],
                    comment=result['message']
                )
            else:
                print(f"  ⚠ No Jira key found for: {test_name}")
        
        print(f"\n✓ Test results updated:")
        print(f"  Passed: {success_count}")
        print(f"  Failed: {fail_count}")
        print(f"  Skipped: {skip_count}")
        print(f"  Total: {len(results)}")
    
    def _update_test_execution(self, cycle_key: str, test_key: str, 
                              status: str, duration: float, comment: str = ""):
        """Update a single test execution in Zephyr"""
        endpoint = f"/rest/atm/1.0/testrun/{cycle_key}/testcase/{test_key}/testresult"
        
        # Map status to Zephyr values
        status_map = {
            'PASS': 'Pass',
            'FAIL': 'Fail',
            'BLOCKED': 'Blocked'
        }
        
        payload = {
            "status": status_map.get(status, 'Fail'),
            "executionTime": int(duration * 1000),  # Convert to milliseconds
        }
        
        if comment:
            payload["comment"] = comment[:500]  # Limit comment length
        
        try:
            self._make_request('POST', endpoint, json=payload)
            print(f"  ✓ Updated {test_key}: {status}")
        except Exception as e:
            print(f"  ✗ Failed to update {test_key}: {e}")
    
    def finalize_test_cycle(self, cycle_key: str, build_number: str, build_url: str):
        """
        Finalize test cycle with summary information
        
        Args:
            cycle_key: Test cycle key
            build_number: Build number from CI/CD
            build_url: URL to build results
        """
        print(f"\nFinalizing test cycle: {cycle_key}")
        
        endpoint = f"/rest/atm/1.0/testrun/{cycle_key}"
        
        summary = (
            f"Automated test execution completed.\n\n"
            f"Build: {build_number}\n"
            f"Build URL: {build_url}\n"
            f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        payload = {
            "status": "Done",
            "description": summary
        }
        
        try:
            self._make_request('PUT', endpoint, json=payload)
            print(f"✓ Test cycle finalized")
            print(f"  View results: {self.base_url}/browse/{cycle_key}")
        except Exception as e:
            print(f"✗ Failed to finalize test cycle: {e}")
    
    def create_defect(self, test_name: str, error_message: str, 
                     cycle_key: str, build_number: str) -> Optional[str]:
        """
        Create a defect in Jira for a failed test
        
        Args:
            test_name: Name of the failed test
            error_message: Error/failure message
            cycle_key: Test cycle key
            build_number: Build number
            
        Returns:
            Defect key if created successfully
        """
        endpoint = "/rest/api/2/issue"
        
        summary = f"[Automated] Test Failure: {test_name}"
        
        description = f"""
h3. Test Failure Details

*Test Name:* {test_name}
*Test Cycle:* {cycle_key}
*Build Number:* {build_number}
*Detected:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

h3. Error Message
{{code}}
{error_message[:1000]}
{{code}}

h3. Investigation Required
This defect was automatically created from a failed automated test execution.
        """
        
        payload = {
            "fields": {
                "project": {
                    "key": self.project_key
                },
                "summary": summary,
                "description": description,
                "issuetype": {
                    "name": "Bug"
                },
                "priority": {
                    "name": "Medium"
                },
                "labels": [
                    "automated-test",
                    "test-failure",
                    f"build-{build_number}"
                ]
            }
        }
        
        try:
            response = self._make_request('POST', endpoint, json=payload)
            data = response.json()
            defect_key = data.get('key')
            
            print(f"✓ Created defect: {defect_key}")
            print(f"  URL: {self.base_url}/browse/{defect_key}")
            
            return defect_key
        except Exception as e:
            print(f"✗ Failed to create defect: {e}")
            return None
    
    def create_defects_from_failures(self, cycle_key: str, build_number: str):
        """Create defects for all failed tests in a cycle"""
        print(f"\nChecking for test failures to create defects...")
        
        # In a real scenario, you would query Zephyr API for failed tests
        # For now, we'll check the JUnit results
        junit_files = []
        for root, dirs, files in os.walk('reports/junit'):
            for file in files:
                if file.endswith('.xml'):
                    junit_files.append(os.path.join(root, file))
        
        total_defects = 0
        
        for junit_file in junit_files:
            if os.path.exists(junit_file):
                results = self.parse_junit_results(junit_file)
                
                for result in results:
                    if result['status'] == 'FAIL':
                        defect_key = self.create_defect(
                            test_name=result['test_name'],
                            error_message=result['message'],
                            cycle_key=cycle_key,
                            build_number=build_number
                        )
                        if defect_key:
                            total_defects += 1
        
        print(f"\n✓ Created {total_defects} defects for failed tests")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Jira/Zephyr Integration Tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create cycle command
    create_parser = subparsers.add_parser('create-cycle', help='Create test cycle')
    create_parser.add_argument('--name', required=True, help='Cycle name')
    create_parser.add_argument('--project', required=True, help='Project key')
    create_parser.add_argument('--version', help='Version/Release')
    
    # Update results command
    update_parser = subparsers.add_parser('update-results', help='Update test results')
    update_parser.add_argument('--cycle', required=True, help='Cycle key')
    update_parser.add_argument('--results', required=True, help='JUnit XML file path')
    update_parser.add_argument('--test-type', default='', help='Test type')
    
    # Finalize cycle command
    finalize_parser = subparsers.add_parser('finalize-cycle', help='Finalize test cycle')
    finalize_parser.add_argument('--cycle', required=True, help='Cycle key')
    finalize_parser.add_argument('--build', required=True, help='Build number')
    finalize_parser.add_argument('--build-url', required=True, help='Build URL')
    
    # Create defects command
    defects_parser = subparsers.add_parser('create-defects', help='Create defects for failures')
    defects_parser.add_argument('--cycle', required=True, help='Cycle key')
    defects_parser.add_argument('--build', required=True, help='Build number')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize integration
    integration = JiraZephyrIntegration()
    
    # Execute command
    try:
        if args.command == 'create-cycle':
            integration.create_test_cycle(
                name=args.name,
                project_key=args.project,
                version=args.version
            )
        
        elif args.command == 'update-results':
            integration.update_test_results(
                cycle_key=args.cycle,
                junit_file=args.results,
                test_type=args.test_type
            )
        
        elif args.command == 'finalize-cycle':
            integration.finalize_test_cycle(
                cycle_key=args.cycle,
                build_number=args.build,
                build_url=args.build_url
            )
        
        elif args.command == 'create-defects':
            integration.create_defects_from_failures(
                cycle_key=args.cycle,
                build_number=args.build
            )
        
        print("\n✓ Command completed successfully")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
