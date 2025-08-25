# Stroke data project

Ce projet contient les fichiers nécessaires au brief Stroke data - Développement d'une API REST et visualisation.

- Pre-processing steps performed :

  1- Check for missing values
  2- Check for nonsense(non-logical) values
  3- Check for duplicate values

- After using the `describe()` method on the numerical columns, we identified some values that seem inconsistent or unreasonable:

  - For example, in the `bmi` column, some values were above 80, which is considered extremely rare or unrealistic for a human being according to medical references.
  - Similarly, in the `avg_glucose_level` column, some values exceeded 300, which could indicate data entry errors or extreme outliers.

  We conducted a quick online search to determine reasonable ranges:

  - For `bmi`, normal values typically range between 15 and 60.
  - For `avg_glucose_level`, values are generally considered normal between 70 and 300.

---

- Rationale for the choices related to addressing missing values :

  Missing values in the bmi column were compensated for by calculating the average within each group made up of the same gender and age group. This option is based on the premise that BMI is influenced by biological factors such as age and gender, so this method provides a more realistic compensation than using an overall average or fixed values

**NOTE** :
During the process of handling missing values in the bmi column, we encountered individual cases that could not be compensated using traditional methods such as groupby(gender, age), due to the scarcity of the age group or insufficient data within the group.

    To address these cases, we created a custom function that compensates for missing values based on a person's characteristics (gender and age) by calculating the average bmi of all individuals who share the same gender and whose ages are within a narrow range around their age (e.g. ±1 year).

---

- A list of Valid values used to detect outliers :

  age: between 0 and 100 years (values above 100 can be considered outliers)
  bmi: between 10 and 60
  avg_glucose_level: between 50 and 300 mg/dL
  hypertension, heart_disease, stroke: binary values (0 or 1 only)
  ever_married: "Yes" or "No"
  work_type: "Private", "Self-employed", "Govt_job", "children", "Never_worked"
  Residence_type: "Urban" or "Rural"
  smoking_status: "never smoked", "formerly smoked", "smokes"

---

- Justifying the choices made to address outliers values:

  During the analysis of the bmi column, 13 values were identified as unusually high (ranging between 64 and 97). After conducting some research, I was unable to determine whether these values were erroneous or simply rare but valid cases, due to a lack of sufficient evidence or reliable references.
  Therefore, I decided to retain these values without modification, pending further information that may support a justified decision.
  Similarly, the smoking_status column contains some entries labeled as 'unknown'. Due to the lack of contextual information or domain-specific knowledge regarding this label, I chose not to impute or modify these values at this stage, to avoid introducing potential bias or misinterpretation.
