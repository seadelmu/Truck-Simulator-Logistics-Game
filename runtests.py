import pytest

def main():
    exit_code = pytest.main(['-v', 'tests/'])
    if exit_code == 0:
        print("All tests passed")
    else:
        print(f"Some tests failed. Exit code: {exit_code}")
        return -1
    
    return 0

if __name__ == "__main__":
    main()