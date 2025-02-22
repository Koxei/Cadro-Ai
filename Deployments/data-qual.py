class DataQualityAssurance:
    def __init__(self):
        """
        Initializes the Data Quality Assurance system.
        """
        self.issues = []
    
    def check_completeness(self, data):
        """
        Checks if any fields in the data are missing.
        """
        missing_fields = [key for key, value in data.items() if value is None or value == ""]
        if missing_fields:
            self.issues.append({"type": "completeness", "missing_fields": missing_fields})
        return not bool(missing_fields)
    
    def check_consistency(self, data1, data2, keys):
        """
        Checks if values of specified keys are consistent between two datasets.
        """
        inconsistencies = {key: (data1.get(key), data2.get(key)) for key in keys if data1.get(key) != data2.get(key)}
        if inconsistencies:
            self.issues.append({"type": "consistency", "inconsistencies": inconsistencies})
        return not bool(inconsistencies)
    
    def check_validity(self, data, validation_rules):
        """
        Validates data based on provided validation rules (e.g., data type, range).
        """
        invalid_entries = {}
        for key, rule in validation_rules.items():
            if key in data and not rule(data[key]):
                invalid_entries[key] = data[key]
        if invalid_entries:
            self.issues.append({"type": "validity", "invalid_entries": invalid_entries})
        return not bool(invalid_entries)
    
    def report_issues(self):
        """
        Returns a summary of detected data quality issues.
        """
        return self.issues

# Example Usage
if __name__ == "__main__":
    data_checker = DataQualityAssurance()
    sample_data = {"name": "Alice", "age": "25", "email": ""}
    
    data_checker.check_completeness(sample_data)
    data_checker.check_validity(sample_data, {"age": lambda x: x.isdigit()})
    
    print(data_checker.report_issues())
