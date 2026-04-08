from src.string_utils import reverse, is_palindrome, word_count, capitalize_words


class TestReverse:
    def test_simple_string(self):
        assert reverse("hello") == "olleh"

    def test_empty_string(self):
        assert reverse("") == ""

    def test_single_char(self):
        assert reverse("a") == "a"

    def test_palindrome(self):
        assert reverse("racecar") == "racecar"


class TestIsPalindrome:
    def test_palindrome(self):
        assert is_palindrome("racecar") is True

    def test_not_palindrome(self):
        assert is_palindrome("hello") is False

    def test_palindrome_with_spaces(self):
        assert is_palindrome("was it a car or a cat I saw") is True

    def test_case_insensitive(self):
        assert is_palindrome("Madam") is True

    def test_empty_string(self):
        assert is_palindrome("") is True


class TestWordCount:
    def test_simple_sentence(self):
        assert word_count("hello world") == 2

    def test_single_word(self):
        assert word_count("hello") == 1

    def test_empty_string(self):
        assert word_count("") == 0

    def test_only_spaces(self):
        assert word_count("   ") == 0

    def test_multiple_spaces(self):
        assert word_count("hello   world") == 2


class TestCapitalizeWords:
    def test_lowercase(self):
        assert capitalize_words("hello world") == "Hello World"

    def test_mixed_case(self):
        assert capitalize_words("hELLO wORLD") == "Hello World"

    def test_single_word(self):
        assert capitalize_words("python") == "Python"

    def test_already_capitalized(self):
        assert capitalize_words("Hello World") == "Hello World"
