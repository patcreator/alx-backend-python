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
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        # Create client instance
        client = GithubOrgClient("testorg")
        
        # Get the property
        result = client._public_repos_url
        
        # Assertion
        self.assertEqual(
            result,
            "https://api.github.com/orgs/testorg/repos"
        )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        # Setup payloads
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = repos_payload

        # Mock _public_repos_url property
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/test/repos"
            
            # Create client instance
            client = GithubOrgClient("test")
            
            # Test without license filter
            repos = client.public_repos()
            
            # Assertions
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )
            
            # Reset mock call count for second test
            mock_get_json.reset_mock()
            mock_public_repos_url.reset_mock()
            
            # Test with license filter
            repos_with_license = client.public_repos(license="mit")
            
            # Assertions
            self.assertEqual(repos_with_license, ["repo1"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )

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


@parameterized_class(('org_payload', 'repos_payload', 
                      'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class for integration tests"""
        # Start patcher for requests.get
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()
        
        # Define side effect for different URLs
        def side_effect(url):
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url", ""):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response
        
        cls.mock_get.side_effect = side_effect

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
