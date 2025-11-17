# =============================================================================
# tests/conftest.py
# =============================================================================
"""Pytest configuration and fixtures"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_test_content():
    """Sample TypeScript test file content"""
    return """
import { Test, TestingModule } from '@nestjs/testing';
import { UserService } from '../user.service';

const mockUser = {
  id: 1,
  name: 'Test User',
  email: 'test@example.com'
};

describe('UserService', () => {
  let service: UserService;
  
  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [UserService],
    }).compile();

    service = module.get<UserService>(UserService);
  });

  describe('create', () => {
    it('should create a user', () => {
      const result = service.create(mockUser);
      expect(result).toBeDefined();
      expect(result.id).toBe(1);
    });
    
    it('should handle validation errors', () => {
      expect(() => service.create({})).toThrow();
    });
  });

  describe('findAll', () => {
    it('should return all users', () => {
      const users = service.findAll();
      expect(users).toBeInstanceOf(Array);
    });
    
    it('should return empty array when no users', () => {
      const users = service.findAll();
      expect(users).toHaveLength(0);
    });
  });
});
"""


@pytest.fixture
def mock_file_path(tmp_path):
    """Create a temporary test file"""
    test_file = tmp_path / "test.spec.ts"
    test_file.write_text("// Test file")
    return test_file