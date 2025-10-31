import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


def clean_data(df: pd.DataFrame, is_train: bool = True) -> pd.DataFrame:
    """Clean the dataset."""

    #----------------------------------------* TRAIN DATASET *------------------------------------
    if is_train:
        # 1- Drop unnecessary columns
        drop_cols = [
            "Patient Id", "Family Name", "Patient First Name", "Father's name",
            "Institute Name", "Location of Institute", "Place of birth",
            "Parental consent", "Test 1", "Test 2", "Test 3", "Test 5"
        ]
        df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)

        # 2- Rename columns
        rename_columns = {
            "Patient Age":"Patient_Age","Genes in mother's side":"Genes_Mother_Side",
            "Inherited from father":"Inherited_from_father","Maternal gene":"Maternal_gene",
            "Paternal gene":"Paternal_gene","Blood cell count (mcL)":"Blood_cell_count(mcL)",
            "Mother's age":"Mother_Age","Father's age":"Father_Age",
            "Respiratory Rate (breaths/min)":"Respiratory_Rate_Breaths_Min","Heart Rate (rates/min)":"Heart_Rates",
            "Follow-up":"Follow_Up","Birth asphyxia":"Birth_Asphyxia",
            "Autopsy shows birth defect (if applicable)":"Autopsy_Birth_Defect",
            "Folic acid details (peri-conceptional)":"Folic_Acid",
            "H/O serious maternal illness":"Maternal_Illness",
            "H/O radiation exposure (x-ray)":"Radiation_Exposure",
            "H/O substance abuse":"Substance_Abuse",
            "Assisted conception IVF/ART":"Assisted_Conception",
            "History of anomalies in previous pregnancies":"History_Previous_Pregnancies",
            "No. of previous abortion":"Previous_Abortion","Birth defects":"Birth_Defects",
            "Test 4":"Test_4","White Blood cell count (thousand per microliter)":"White_Blood_Cell",
            "Blood test result":"Blood_Test_Result",
            "Symptom 1":"Symptom_1","Symptom 2":"Symptom_2","Symptom 3":"Symptom_3",
            "Symptom 4":"Symptom_4","Symptom 5":"Symptom_5",
            "Genetic Disorder":"Genetic_Disorder","Disorder Subclass":"Disorder_Subclass"
        }
        df.rename(columns=rename_columns, inplace=True)

        # 3- Replace special text values with NaN
        replace_map = {
            "Gender":["Ambiguous"],
            "Birth_Asphyxia": ["No record", "Not available"],
            "Autopsy_Birth_Defect": ["Not applicable","None"],
            "Radiation_Exposure": ["Not applicable", "-"],
            "Substance_Abuse": ["Not applicable", "-"]
        }
        for col, values in replace_map.items():
            if col in df.columns:
                df[col] = df[col].replace(values, np.nan)

        # 4- Drop specific columns
        drop_extra = ["Autopsy_Birth_Defect", "Birth_Asphyxia", "Radiation_Exposure", "Substance_Abuse"]
        df.drop(columns=[c for c in drop_extra if c in df.columns], inplace=True)

        # 5- Drop rows with missing Test_4
        if "Test_4" in df.columns:
            df.dropna(subset=['Test_4'], inplace=True)

        # 6- Fill missing numeric columns
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            df[numeric_cols] = SimpleImputer(strategy='mean').fit_transform(df[numeric_cols])

        # 7- Fill missing categorical columns
        categorical_cols = df.select_dtypes(exclude='number').columns
        exclude_targets = ['Genetic_Disorder', 'Disorder_Subclass']
        categorical_cols = [c for c in categorical_cols if c not in exclude_targets]
        if len(categorical_cols) > 0:
            df[categorical_cols] = SimpleImputer(strategy='most_frequent').fit_transform(df[categorical_cols])

        # Additional cleaning for Respiratory_Rate_Breaths_Min
        if "Respiratory_Rate_Breaths_Min" in df.columns:
            df["Respiratory_Rate_Breaths_Min"] = (
                df["Respiratory_Rate_Breaths_Min"]
                .astype(str)
                .str.replace(r"\s*\(.*\)", "", regex=True)
                )

        # 8- Fill missing Genetic_Disorder based on Disorder_Subclass
        if "Genetic_Disorder" in df.columns and "Disorder_Subclass" in df.columns:
            def fill_Genetic_Disorder(row):
                if pd.isnull(row['Genetic_Disorder']):
                    mapping = {
                        "Leber's hereditary op": 'Mitochondrial genetic inheritance disorders',
                        "Cystic fibrosis": 'Single-gene inheritance diseases',
                        "Diabetes": 'Multifactorial genetic inheritance disorders',
                        "Leigh syndrome": 'Mitochondrial genetic inheritance disorders',
                        "Cancer": 'Multifactorial genetic inheritance disorders',
                        "Tay-Sachs": 'Single-gene inheritance diseases',
                        "Mitochondrial myopathy": 'Mitochondrial genetic inheritance disorders',
                        "Hemochromatosis": 'Single-gene inheritance diseases',
                        "Leber's hereditary optic neuropathy": 'Mitochondrial genetic inheritance disorders',
                        "Alzheimer's": 'Multifactorial genetic inheritance disorders'
                    }
                    return mapping.get(row['Disorder_Subclass'], row['Genetic_Disorder'])
                return row['Genetic_Disorder']

            df['Genetic_Disorder'] = df.apply(fill_Genetic_Disorder, axis=1)
            df.dropna(subset=['Genetic_Disorder'], inplace=True)

    #----------------------------------------* TEST DATASET *------------------------------------
    else:

        # 1- Drop unnecessary columns
        drop_cols = [
            "Patient Id", "Family Name", "Patient First Name", "Father's name",
            "Institute Name", "Location of Institute", "Place of birth",
            "Parental consent", "Test 1", "Test 2", "Test 3", "Test 5",
            "Autopsy_Birth_Defect", "Birth_Asphyxia", "Radiation_Exposure", "Substance_Abuse",
            "Autopsy shows birth defect (if applicable)", "Birth asphyxia",
            "H/O radiation exposure (x-ray)", "H/O substance abuse"
        ]
        df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)

        # 2- Rename columns
        rename_columns = {
            "Patient Age":"Patient_Age",
            "Genes in mother's side":"Genes_Mother_Side","Inherited from father":"Inherited_from_father",
            "Maternal gene":"Maternal_gene","Paternal gene":"Paternal_gene","Blood cell count (mcL)":"Blood_cell_count(mcL)",
            "Mother's age":"Mother_Age","Father's age":"Father_Age",
            "Respiratory Rate (breaths/min)":"Respiratory_Rate_Breaths_Min","Heart Rate (rates/min)":"Heart_Rates",
            "Follow-up":"Follow_Up","Folic acid details (peri-conceptional)":"Folic_Acid",
            "H/O serious maternal illness":"Maternal_Illness","Assisted conception IVF/ART":"Assisted_Conception",
            "History of anomalies in previous pregnancies":"History_Previous_Pregnancies",
            "No. of previous abortion":"Previous_Abortion","Birth defects":"Birth_Defects",
            "Test 4":"Test_4","White Blood cell count (thousand per microliter)":"White_Blood_Cell",
            "Blood test result":"Blood_Test_Result","Symptom 1":"Symptom_1","Symptom 2":"Symptom_2",
            "Symptom 3":"Symptom_3","Symptom 4":"Symptom_4","Symptom 5":"Symptom_5"}
        df.rename(columns=rename_columns, inplace=True)

        # 3- Replace placeholders with NaN
        nan_replace_map = {
            "Respiratory_Rate_Breaths_Min": ["-99"],
            "Heart_Rates": ["-99"],
            "Test_4": ["-99"],
            "Follow_Up": ["-99"],
            "Gender": ["-99", "Ambiguous"],
            "Folic_Acid": ["-99"],
            "Maternal_Illness": ["-99"],
            "Assisted_Conception": ["-99"],
            "History_Previous_Pregnancies": ["-99"],
            "Previous_Abortion": ["-99"],
            "Birth_Defects": ["-99"],
            "White_Blood_Cell": ["-99"],
            "Blood_Test_Result": ["-99"]
            }

        # Extend values list to also include numeric -99 and -99.0
        for col, values in nan_replace_map.items():
            expanded_values = set(values + [-99, -99.0])
            if col in df.columns:
                df[col] = df[col].replace(list(expanded_values), np.nan)
        # Additional cleaning for Respiratory_Rate_Breaths_Min
        if "Respiratory_Rate_Breaths_Min" in df.columns:
            df["Respiratory_Rate_Breaths_Min"] = (
                df["Respiratory_Rate_Breaths_Min"]
                .astype(str)
                .str.replace(r"\s*\(.*\)", "", regex=True)
                )

        # 4- Fill missing numeric and categorical values
        imputer = SimpleImputer(strategy='mean')
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

        cat_imputer = SimpleImputer(strategy='most_frequent')
        categorical_cols = df.select_dtypes(exclude='number').columns
        if len(categorical_cols) > 0:
            df[categorical_cols] = cat_imputer.fit_transform(df[categorical_cols])

        print("✅ Data cleaned")

    return df
