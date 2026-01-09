#!/usr/bin/env python3
"""Test client module
"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import Mock, patch, PropertyMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value"""
        # Setup mock
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        # Create client instance
        client = GithubOrgClient(org_name)
        
        # Call the method
        result = client.org
        
        # Assertions
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test GithubOrgClient._public_repos_url property"""
        # Setup mock
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        mock_org.return_value = test_payload

        # Create client instance
        client = GithubOrgClient("testorg")
        
        # Get the property
        result = client._public_repos_url
        
        # Assertion
        self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        # Setup test data
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        mock_get_json.return_value = test_payload

        # Create client instance and mock _public_repos_url
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test/repos"
        ) as mock_url:
            client = GithubOrgClient("test")
            
            # Test without license filter
            repos = client.public_repos()
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)
            
            # Test that mocked methods were called correctly
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")
            
            # Reset mocks for second test
            mock_get_json.reset_mock()
            mock_url.reset_mock()
            
            # Test with license filter
            repos_with_license = client.public_repos(license="mit")
            expected_repos_with_license = ["repo1"]
            self.assertEqual(repos_with_license, expected_repos_with_license)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": None}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license static method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class for integration tests"""
        # Start patcher for requests.get
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()
        
        # Configure the mock
        cls.mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload
        ]

    @classmethod
    def tearDownClass(cls):
        """Tear down class after tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos without license"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with apache-2.0 license"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
