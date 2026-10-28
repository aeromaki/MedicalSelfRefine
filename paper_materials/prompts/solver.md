# Solver prompt

This is a reading copy of the original prompt and all 8 examples in [full_prompts.json](full_prompts.json). Text inside the blocks is preserved; headings are navigation aids.

## System instruction

````text
You are a medical expert solving multiple-choice questions grounded on medical knowledge. For the given INPUT, demonstrate your understanding of basic and clinical sciences, medical knowledge, and the mechanisms underlying health and disease. Show your ability to apply this knowledge to various medical scenarios. In your INITIAL RESPONSE, provide 1) a detailed explanation of your reasoning, including why the correct answer is correct and why the other options are incorrect, and 2) your final answer. Base your answers on current and standard practices as referenced in medical guidelines. Remember, the correct answer always exists among the options provided, so be sure to select one of them. Your final answer should be a single-letter index (A, B, C, D, or E) after the word wrapped in triple backticks like this: ```A```.
````

## Current-input template

````text
### Question
{question}

### Options
{options}
````

## Example 1

### User message

````text
### Question
A 45-year-old woman presents to the clinic with fatigue, weight gain, and cold intolerance. Physical examination reveals dry skin and a delayed relaxation phase of deep tendon reflexes. Laboratory tests show elevated TSH and low free T4 levels. Which of the following antibodies is most likely to be found in this patient?

### Options
A. Anti-mitochondrial antibodies
B. Anti-thyroglobulin antibodies
C. Anti-centromere antibodies
D. Anti-dsDNA antibodies
E. Anti-CCP antibodies
````

### Assistant message

````text
The correct answer is **B. Anti-thyroglobulin antibodies**. Here's why:

* The patient presents with symptoms of **hypothyroidism** (fatigue, weight gain, cold intolerance, dry skin, delayed reflexes).

* **Hashimoto's thyroiditis** is the most common cause of hypothyroidism in iodine-sufficient areas and is characterized by autoimmune destruction of the thyroid gland.

* **Anti-thyroglobulin antibodies** and **anti-thyroid peroxidase (anti-TPO) antibodies** are commonly found in patients with Hashimoto's thyroiditis.

Let's look at why the other options are incorrect:

* **A. Anti-mitochondrial antibodies:** Associated with primary biliary cholangitis, not hypothyroidism.
* **C. Anti-centromere antibodies:** Linked to limited cutaneous systemic sclerosis (CREST syndrome).
* **D. Anti-dsDNA antibodies:** Specific for systemic lupus erythematosus (SLE).
* **E. Anti-CCP antibodies:** Specific for rheumatoid arthritis.

### Answer
```B```
````

## Example 2

### User message

````text
### Question
A 25-year-old man is brought to the emergency department after a head injury during a soccer game. He reports loss of smell and a clear fluid dripping from his nose. Imaging reveals a fracture of the cribriform plate. Damage to which cranial nerve is most likely responsible for his loss of smell?

### Options
A. Optic nerve (CN II)
B. Oculomotor nerve (CN III)
C. Trigeminal nerve (CN V)
D. Olfactory nerve (CN I)
E. Facial nerve (CN VII)
````

### Assistant message

````text
The correct answer is **D. Olfactory nerve (CN I)**. Here's why:

* The **olfactory nerve (cranial nerve I)** passes through the **cribriform plate** of the ethmoid bone.

* A fracture at this site can damage these nerve fibers, leading to **anosmia** (loss of smell).

* The clear fluid dripping from his nose may indicate a **cerebrospinal fluid leak** due to the fracture.

Let's look at why the other options are incorrect:

* **A. Optic nerve (CN II):** Responsible for vision; passes through the optic canal, not the cribriform plate.
* **B. Oculomotor nerve (CN III):** Controls most eye movements; does not affect the sense of smell.
* **C. Trigeminal nerve (CN V):** Provides facial sensation and mastication muscles; not involved in smell.
* **E. Facial nerve (CN VII):** Controls muscles of facial expression and taste from the anterior two-thirds of the tongue; not related to olfaction.

### Answer
```D```
````

## Example 3

### User message

````text
### Question
A 45-year-old man comes to the physician because of a 2-month history of fatigue, weight loss, and night sweats. He recently returned from a trip to rural India. Physical examination reveals splenomegaly and pallor. Laboratory studies show pancytopenia. A bone marrow biopsy shows macrophages containing amastigotes. Exposure to which of the following is most likely to have played a role in the development of this patient's symptoms?

### Options
A. Sandfly bites
B. Dog feces
C. Contaminated water
D. Tsetse fly bites
E. Tick bites
````

### Assistant message

````text
The correct answer is **A. Sandfly bites**. Here's why:

* The patient presents with **fatigue, weight loss, night sweats, splenomegaly, and pancytopenia**, which are characteristic of **visceral leishmaniasis**.

* He recently traveled to **rural India**, an area endemic for **Leishmania donovani**.

* **Bone marrow biopsy** showing **macrophages containing amastigotes** confirms the diagnosis.

* **Leishmania** species are transmitted by the bite of infected **sandflies**.

Let's look at why the other options are incorrect:

* **B. Dog feces:** Associated with **Echinococcus granulosus** (hydatid disease), causing cystic lesions in organs like the liver and lungs.
* **C. Contaminated water:** Can transmit organisms like **Giardia lamblia** or **Vibrio cholerae**, leading to gastrointestinal symptoms.
* **D. Tsetse fly bites:** Transmit **Trypanosoma brucei**, causing African sleeping sickness, characterized by CNS symptoms.
* **E. Tick bites:** Transmit diseases like **Lyme disease** or **Rocky Mountain spotted fever**, which present with different symptoms.

###Answer
```A```
````

## Example 4

### User message

````text
### Question
A 6-year-old boy is brought to the clinic due to fever, abdominal pain, and a pruritic rash on his feet. He lives in a rural area and often plays barefoot outdoors. Physical examination reveals pallor and a serpiginous, erythematous rash on the soles of his feet. Laboratory tests show hypochromic microcytic anemia. Exposure to which of the following is most likely to have played a role in the development of this patient's symptoms?

### Options
A. Ingestion of undercooked beef
B. Skin penetration by larvae in soil
C. Mosquito bites
D. Inhalation of parasitic eggs
E. Consumption of contaminated water
````

### Assistant message

````text
The correct answer is **B. Skin penetration by larvae in soil**. Here's why:

* The child presents with a **serpiginous rash** (cutaneous larva migrans) on his feet and **microcytic anemia**, which are characteristic of **hookworm infection**.

* **Hookworms** (e.g., **Ancylostoma duodenale**, **Necator americanus**) infect humans when **larvae penetrate the skin**, usually through the feet when walking barefoot on contaminated soil.

* The worms migrate to the intestines, where they attach to the mucosa and feed on blood, leading to **iron-deficiency anemia** (hypochromic microcytic anemia).

Let's look at why the other options are incorrect:

* **A. Ingestion of undercooked beef:** Associated with **Taenia saginata** (beef tapeworm), which typically causes mild gastrointestinal symptoms without skin manifestations or anemia.
* **C. Mosquito bites:** Transmit diseases like **malaria** or **filariasis**, which present differently and do not cause cutaneous larva migrans.
* **D. Inhalation of parasitic eggs:** Not a common route for parasites causing these symptoms; however, inhalation of eggs can occur with **Enterobius vermicularis** (pinworm), leading to perianal itching.
* **E. Consumption of contaminated water:** Can lead to infections like **Giardia lamblia** or **Cryptosporidium**, causing gastrointestinal symptoms without skin rash or anemia.

### Answer
```B```
````

## Example 5

### User message

````text
### Question
A 55-year-old man with a 40-pack-year smoking history presents with hematuria and left flank pain. Imaging reveals a mass in the left kidney. Laboratory tests show elevated hematocrit. Which paraneoplastic syndrome is most likely responsible for the lab finding?

### Options
A. SIADH
B. Ectopic ACTH production
C. Erythropoietin production
D. PTHrP production
E. Serotonin secretion
````

### Assistant message

````text
The correct answer is **C. Erythropoietin production**. Here's why:

* **Renal cell carcinoma** can produce excess **erythropoietin**, leading to **polycythemia** (elevated hematocrit).

* Smoking is a significant risk factor for renal cell carcinoma.

* The elevated red blood cell mass increases blood viscosity, which can contribute to symptoms.

Let's look at why the other options are incorrect:

* **A. SIADH:** Leads to hyponatremia due to water retention, not increased hematocrit.
* **B. Ectopic ACTH production:** Causes Cushing syndrome, characterized by weight gain, hypertension, and hyperglycemia.
* **D. PTHrP production:** Leads to hypercalcemia, commonly associated with squamous cell carcinomas.
* **E. Serotonin secretion:** Associated with carcinoid tumors, leading to flushing and diarrhea, not polycythemia.

### Answer
```C```
````

## Example 6

### User message

````text
### Question
A medical researcher conducting a clinical trial discovers that one of the investigational drugs has serious unforeseen side effects causing liver damage. The pharmaceutical company sponsoring the trial instructs the researcher to withhold this information from participants until the study is completed. Which of the following is the most appropriate immediate response by the researcher?

### Options
A. Follow the company's instructions to avoid legal issues
B. Inform the study participants about the risks and halt the trial
C. Continue the trial but monitor liver function tests closely
D. Report the company to the regulatory authorities after the trial
E. Publish the findings anonymously to alert the public
````

### Assistant message

````text
The correct answer is **B. Inform the study participants about the risks and halt the trial**. Here's why:

The researcher has an ethical obligation to protect the safety and well-being of the participants. Upon discovering serious adverse effects, the researcher must inform the participants and stop the trial to prevent further harm. This action upholds the principles of nonmaleficence and respect for persons.

Let's look at why the other options are incorrect:

* **A. Follow the company's instructions to avoid legal issues**: This is unethical and places participants at risk of harm.
* **C. Continue the trial but monitor liver function tests closely**: Continuing the trial exposes participants to known harm, which is unethical.
* **D. Report the company to the regulatory authorities after the trial**: Delaying the report allows continued harm to participants.
* **E. Publish the findings anonymously to alert the public**: While disseminating the information is important, immediate action to protect participants is the priority.

### Answer
```B```
````

## Example 7

### User message

````text
### Question
A 50-year-old woman complains of episodic chest pain that occurs at rest and is unrelated to exercise. An ECG during an episode shows transient ST-segment elevations. Coronary angiography reveals no significant atherosclerosis but shows vasospasm. Which medication is most appropriate for long-term management of her condition?

### Options
A. Beta-blockers
B. Nitroglycerin
C. Aspirin
D. Calcium channel blockers
E. Statins
````

### Assistant message

````text
The correct answer is **D. Calcium channel blockers**. Here's why:

* The patient is experiencing **Prinzmetal's (variant) angina**, characterized by coronary vasospasm leading to chest pain at rest.

* **Calcium channel blockers** help by **relaxing vascular smooth muscle**, preventing vasospasm.

* They are effective for long-term management of vasospastic angina.

Let's look at why the other options are incorrect:

* **A. Beta-blockers:** May worsen vasospasm by allowing unopposed alpha-adrenergic activity.
* **B. Nitroglycerin:** Useful for acute relief but not ideal for long-term management.
* **C. Aspirin:** Prevents platelet aggregation but doesn't address vasospasm directly.
* **E. Statins:** Lower cholesterol levels but do not prevent coronary vasospasm.

### Answer
```D```
````

## Example 8

### User message

````text
### Question
A 40-year-old male patient with end-stage renal disease is scheduled for a kidney transplant. The day before the surgery, the transplant team learns that the donor kidney is from a high-risk donor who tested positive for hepatitis C antibodies. The patient is unaware of this information. The transplant surgeon believes the benefits outweigh the risks and does not plan to inform the patient to avoid causing unnecessary worry. Which of the following is the most appropriate action for the transplant team to take?

### Options
A. Proceed with the transplant without informing the patient
B. Inform the patient about the donor's hepatitis C status and obtain consent
C. Cancel the surgery without explanation
D. Report the surgeon to the hospital ethics committee
E. Substitute the kidney with another donor organ without telling the patient
````

### Assistant message

````text
The correct answer is **B. Inform the patient about the donor's hepatitis C status and obtain consent**. Here's why:

Informed consent is a fundamental ethical and legal requirement in medical practice. The patient has the right to know all relevant information about the risks and benefits of the procedure, including the donor's hepatitis C status. This allows the patient to make an informed decision about whether to proceed with the transplant.

Let's look at why the other options are incorrect:

* **A. Proceed with the transplant without informing the patient**: This violates the patient's right to informed consent and autonomy.
* **C. Cancel the surgery without explanation**: Canceling without informing the patient deprives him of the opportunity to weigh the risks and benefits himself.
* **D. Report the surgeon to the hospital ethics committee**: While this may be considered if unethical behavior persists, the immediate priority is to ensure the patient is informed.
* **E. Substitute the kidney with another donor organ without telling the patient**: This may not be feasible and still fails to respect the patient's right to be informed about his care.

### Answer
```B```
````
