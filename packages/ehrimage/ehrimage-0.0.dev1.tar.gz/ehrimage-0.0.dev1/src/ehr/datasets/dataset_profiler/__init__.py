# Created by san at 2/3/24
"""
- Vision:
    * use dataset profiler achieve eventual code-free exploratory cohort analysis
- Roadmap
    * infer table schema (nice to be automated, but can move forward by manually set it up)
        * column names
        * data type (string, numeric, datetime)
            * numeric: numeric-discrete, numeric-continuous
            * string: string-categorical, string-free
        * relationship among tables (visualize links among tables)
    * analytical check
        * column analytical type:
            * key: column that link tables
            * index: column that is id but not key. 
            * feature: columns with analytical data. worth to profile deeper
            * TBD
        * `std` is a very useful indicator to differentiate "numeric id" from "numeric features". Often id column has very big std
    * quality check
        * universal analysis given a vocab={"domain": {"vocab": {"concept_name": [codes]}}}:
            * for each table: n_records, n_codes, n_patients
            * for each code: n_records, n_patients, corresponding name
            * n_not_na
            * n_unique
        * data type specific analysis:
            * ID columns:
                * distribution of "number of record per patient"
                * distribution of "number of unique values per patient"
                * top N frequent values
            * date columns:
                * n_valid
                * min, max
            * numeric columns:
                * distribution (histogram with percentile)
            * text columns
                * top N frequent values
        * source table specific
            * invalid values profile
                * non-numeric
                * date

- Reference:
    * [TFDV](https://www.tensorflow.org/tfx/data_validation/get_started)
    * [pandas profiling, now YData profiling](https://docs.profiling.ydata.ai/latest/)
    * [OHDSI](https://www.ohdsi.org/2019-tutorial-data-quality/)
"""