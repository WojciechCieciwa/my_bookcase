class FileProcessor:
    """
    Handles file loading and basic text retrieval operations.
    """
    def __init__(self):
        self.lines = []

    def open_file(self, filename):
        """
        Opens the specified text file and reads its lines into a list.
        """
        with open(filename, 'r', encoding='utf-8') as file:
            self.lines = file.readlines()

    def get_total_lines(self):
        """
        Returns the total number of lines loaded.
        """
        return len(self.lines)

    def get_line(self, index):
        """
        Returns a single line at the specified index (empty if out of range).
        """
        if 0 <= index < len(self.lines):
            return self.lines[index]
        return ""

    def get_lines_in_range(self, start, count=10):
        """
        Returns up to `count` lines starting from `start`.
        """
        end = start + count
        return self.lines[start:end]
