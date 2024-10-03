def capitalize_words(s):
    """Capitalize the first letter of each word in a string."""
    return ' '.join(word.capitalize() for word in s.split())

def reverse_string(s):
    """Return the reverse of the input string."""
    return s[::-1]

def count_vowels(s):
    """Return the count of vowels in the input string."""
    return sum(1 for char in s if char.lower() in 'aeiou')
