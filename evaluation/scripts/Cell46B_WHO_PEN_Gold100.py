# Cell 46B — WHO PEN 100-question source-grounded gold candidate set
# NOTE:
# - 100 questions distributed across all 22 numbered WHO PEN modules.
# - This is source-grounded and anchor-validated, but it is NOT clinician-reviewed Human Gold yet.
# - Only cases whose answer anchor resolves inside the corrected leaf corpus are accepted.

import json
import re
from pathlib import Path
import pandas as pd

GOLD_100_CANDIDATES = [
  {
    "question_id": "Q001",
    "module_id": "1.1",
    "question_type": "concept",
    "question": "According to WHO PEN, what three broad categories are considered determinants of health?",
    "reference_answer": "The social and economic environment, the physical environment, and individual characteristics and behaviour.",
    "answer_anchor": "social and economic environment"
  },
  {
    "question_id": "Q002",
    "module_id": "1.1",
    "question_type": "risk_factor",
    "question": "Which lifestyle factors does WHO PEN describe as modifiable determinants of health?",
    "reference_answer": "Diet, level of exercise, alcohol consumption, and smoking status.",
    "answer_anchor": "Diet, level of exercise, alcohol consumption and smoking status"
  },
  {
    "question_id": "Q003",
    "module_id": "1.1",
    "question_type": "contrast",
    "question": "How does WHO PEN distinguish an individual-level prevention approach from a population-level approach?",
    "reference_answer": "Individual-level approaches target individual factors such as knowledge, attitudes and beliefs; population-level approaches address broader social and environmental circumstances that influence behaviour.",
    "answer_anchor": "Population-level approaches address broader social and environmental circumstances"
  },
  {
    "question_id": "Q004",
    "module_id": "1.1",
    "question_type": "concept",
    "question": "What does WHO PEN mean by NCD 'best buy' interventions?",
    "reference_answer": "Evidence-based interventions that are highly cost-effective, feasible and appropriate to implement within local health-system constraints.",
    "answer_anchor": "highly cost-effective but also feasible and appropriate"
  },
  {
    "question_id": "Q005",
    "module_id": "1.2",
    "question_type": "care_model",
    "question": "What patient-care principle does WHO PEN recommend when managing chronic diseases or risk conditions?",
    "reference_answer": "Develop a treatment partnership with the patient and focus on the patient's concerns and priorities.",
    "answer_anchor": "Develop a treatment partnership with your patient"
  },
  {
    "question_id": "Q006",
    "module_id": "1.2",
    "question_type": "care_model",
    "question": "Why is an integrated approach to NCD care particularly important in low-resource settings?",
    "reference_answer": "It helps limited resources be used efficiently by integrating a core set of interventions with primary health-care services.",
    "answer_anchor": "limited resources are used efficiently"
  },
  {
    "question_id": "Q007",
    "module_id": "1.2",
    "question_type": "purpose",
    "question": "What is the aim of WHO PEN as described in the PHC module?",
    "reference_answer": "To provide an equitable framework for scale-up toward universal access and close the gap between needed and currently available essential NCD interventions in PHC.",
    "answer_anchor": "closing the gap between what is needed and what is currently available"
  },
  {
    "question_id": "Q008",
    "module_id": "1.2",
    "question_type": "purpose",
    "question": "What is the vision of WHO PEN?",
    "reference_answer": "Effective and equitable prevention and care for people with NCDs.",
    "answer_anchor": "Effective and equitable prevention and care for people with NCDs"
  },
  {
    "question_id": "Q009",
    "module_id": "2.1",
    "question_type": "definition",
    "question": "How long is a brief intervention for healthy-lifestyle counselling in WHO PEN?",
    "reference_answer": "A brief intervention is a short interaction lasting about 3–20 minutes.",
    "answer_anchor": "short interaction of 3–20 minutes"
  },
  {
    "question_id": "Q010",
    "module_id": "2.1",
    "question_type": "framework",
    "question": "What are the five steps of the 5A's behavioural counselling intervention?",
    "reference_answer": "Ask, Advise, Assess, Assist, and Arrange.",
    "answer_anchor": "Ask, Advise, Assess, Assist, and Arrange"
  },
  {
    "question_id": "Q011",
    "module_id": "2.1",
    "question_type": "framework",
    "question": "What are the five components of the 5R's intervention?",
    "reference_answer": "Relevance, Risks, Rewards, Roadblocks, and Repetition.",
    "answer_anchor": "Relevance, Risks, Rewards, Roadblocks, and Repetition"
  },
  {
    "question_id": "Q012",
    "module_id": "2.1",
    "question_type": "selection",
    "question": "When should the 5A's versus the 5R's be used in healthy-lifestyle counselling?",
    "reference_answer": "The 5A's are used for patients ready to change; the 5R's are used to increase motivation in patients not yet ready to change.",
    "answer_anchor": "an approach to help patients/clients who are ready to change their behaviour"
  },
  {
    "question_id": "Q013",
    "module_id": "2.1",
    "question_type": "behaviour_change",
    "question": "Does relapse necessarily mean failure in the WHO PEN stages-of-change model?",
    "reference_answer": "No. Relapse can occur at any point, and many people make several attempts before maintaining a new behaviour long term.",
    "answer_anchor": "Relapse into an old behaviour does not necessarily mean a failure to change"
  },
  {
    "question_id": "Q014",
    "module_id": "2.2",
    "question_type": "screening",
    "question": "How often should primary-care providers ask patients about tobacco use?",
    "reference_answer": "At every patient visit, with tobacco-use status documented in the medical record.",
    "answer_anchor": "ask about tobacco use at EVERY patient visit"
  },
  {
    "question_id": "Q015",
    "module_id": "2.2",
    "question_type": "procedure",
    "question": "What does the STAR quit-plan approach ask a tobacco user to do?",
    "reference_answer": "Set a quit date (ideally within two weeks), tell family and friends and ask for support, anticipate challenges, and remove tobacco products from the personal environment while making the home smoke-free.",
    "answer_anchor": "Set a quit date, ideally within 2 weeks"
  },
  {
    "question_id": "Q016",
    "module_id": "2.2",
    "question_type": "motivation",
    "question": "What should a health-care worker do in the 'Repetition' component of the tobacco 5R's?",
    "reference_answer": "Reassess readiness to quit and repeat the motivational intervention at later visits if the patient is still not ready.",
    "answer_anchor": "The motivational intervention should be repeated every time an unmotivated patient visits"
  },
  {
    "question_id": "Q017",
    "module_id": "2.2",
    "question_type": "clinical_fact",
    "question": "How long do nicotine withdrawal symptoms normally last according to WHO PEN?",
    "reference_answer": "They are normally temporary, lasting about 2–4 weeks.",
    "answer_anchor": "normally temporary (2–4 weeks)"
  },
  {
    "question_id": "Q018",
    "module_id": "2.2",
    "question_type": "benefit",
    "question": "About one year after quitting smoking, how does heart-attack and angina risk compare with that of a smoker?",
    "reference_answer": "It is about half that of a smoker.",
    "answer_anchor": "within 1 year the person’s risk of heart attack and angina is about half that of a smoker"
  },
  {
    "question_id": "Q019",
    "module_id": "2.3",
    "question_type": "table_numeric",
    "question": "What intervention is listed for an AUDIT score of 0–7?",
    "reference_answer": "Alcohol education.",
    "answer_anchor": "AUDIT score: 0-7 | Intervention: Alcohol education"
  },
  {
    "question_id": "Q020",
    "module_id": "2.3",
    "question_type": "table_numeric",
    "question": "What intervention is listed for an AUDIT score of 8–15?",
    "reference_answer": "Simple advice.",
    "answer_anchor": "8–15 Simple advice"
  },
  {
    "question_id": "Q021",
    "module_id": "2.3",
    "question_type": "table_numeric",
    "question": "How is an AUDIT score of 16–19 managed?",
    "reference_answer": "Simple advice plus brief counselling and continued monitoring.",
    "answer_anchor": "16-19 | Intervention: Simple advice plus brief counseling and continued monitoring"
  },
  {
    "question_id": "Q022",
    "module_id": "2.3",
    "question_type": "table_numeric",
    "question": "What is listed for an AUDIT score of 20–40?",
    "reference_answer": "Referral to a specialist.",
    "answer_anchor": "20–40 Referral to specialist"
  },
  {
    "question_id": "Q023",
    "module_id": "2.3",
    "question_type": "diagnostic_criteria",
    "question": "Under the ICD-10 criteria described in WHO PEN, how many manifestations support alcohol dependence and over what time pattern?",
    "reference_answer": "Three or more manifestations occurring together for at least one month, or repeatedly together within a 12-month period if episodes persist for less than one month.",
    "answer_anchor": "Three or more of the following manifestations should have occurred together for at least one month"
  },
  {
    "question_id": "Q024",
    "module_id": "2.4",
    "question_type": "nutrition",
    "question": "How many portions of fruit and vegetables per day does WHO PEN advise?",
    "reference_answer": "At least five portions per day.",
    "answer_anchor": "Eat at least 5 portions of fruit and vegetables per day"
  },
  {
    "question_id": "Q025",
    "module_id": "2.4",
    "question_type": "nutrition",
    "question": "Give one example WHO PEN provides for a single portion of fruit or vegetables.",
    "reference_answer": "Examples include one orange, apple, mango or banana, or three tablespoons of cooked vegetables.",
    "answer_anchor": "1 portion = 1 orange, apple, mango, banana, or 3 tablespoons of cooked vegetables"
  },
  {
    "question_id": "Q026",
    "module_id": "2.4",
    "question_type": "nutrition",
    "question": "Do potatoes, sweet potatoes, cassava and other starchy roots count as one of the fruit-and-vegetable portions?",
    "reference_answer": "No. WHO PEN says these starchy tubers or roots do not count as one of the portions.",
    "answer_anchor": "starchy tubers or roots do not count as one of these portions"
  },
  {
    "question_id": "Q027",
    "module_id": "2.4",
    "question_type": "nutrition",
    "question": "Which types of unhealthy food items are highlighted when reviewing a typical local menu?",
    "reference_answer": "Foods high in salt, saturated fats and sugar.",
    "answer_anchor": "high in salt, saturated fats and sugar"
  },
  {
    "question_id": "Q028",
    "module_id": "2.5",
    "question_type": "numeric",
    "question": "What weekly amount of moderate physical activity does WHO PEN recommend for adults?",
    "reference_answer": "At least 150 minutes of moderate physical activity per week.",
    "answer_anchor": "Adults should accumulate at least 150 minutes of moderate physical activity"
  },
  {
    "question_id": "Q029",
    "module_id": "2.5",
    "question_type": "numeric",
    "question": "How much moderate physical activity should generally be achieved in a day?",
    "reference_answer": "At least 30 minutes in a day.",
    "answer_anchor": "At least 30 minutes of moderate physical activity should be achieved in a day"
  },
  {
    "question_id": "Q030",
    "module_id": "2.5",
    "question_type": "numeric",
    "question": "What daily physical-activity target is given for children and youth aged 5–17 years?",
    "reference_answer": "At least 60 minutes of moderate- to vigorous-intensity physical activity each day.",
    "answer_anchor": "aged 5–17 years should accumulate at least 60 minutes"
  },
  {
    "question_id": "Q031",
    "module_id": "2.5",
    "question_type": "definition",
    "question": "How does WHO PEN distinguish exercise from physical activity?",
    "reference_answer": "Exercise is a planned, structured, repetitive and purposeful subcategory of physical activity; physical activity also includes movement during work, transport, chores, play and recreation.",
    "answer_anchor": "Exercise is a subcategory of physical activity that is planned, structured, repetitive and purposeful"
  },
  {
    "question_id": "Q032",
    "module_id": "2.6",
    "question_type": "table_numeric",
    "question": "What adult BMI range is classified as normal in WHO PEN?",
    "reference_answer": "18.5–24.9 kg/m².",
    "answer_anchor": "Normal 18.5–24.9 kg/m2"
  },
  {
    "question_id": "Q033",
    "module_id": "2.6",
    "question_type": "table_numeric",
    "question": "At what BMI is an adult classified as obese?",
    "reference_answer": "BMI ≥30.0 kg/m².",
    "answer_anchor": "Obese ≥30.0 kg/m2"
  },
  {
    "question_id": "Q034",
    "module_id": "2.6",
    "question_type": "assessment",
    "question": "What measurements does the 5A's obesity intervention tell the health worker to assess?",
    "reference_answer": "Health status, BMI, waist circumference, hip circumference and waist–hip ratio, along with drivers of obesity and readiness to change.",
    "answer_anchor": "Assess the health status, BMI, waist circumference, hip circumference, waist–hip ratio"
  },
  {
    "question_id": "Q035",
    "module_id": "2.6",
    "question_type": "risk_factor",
    "question": "What is the fundamental cause of overweight and obesity described in WHO PEN?",
    "reference_answer": "An energy imbalance between calories consumed and calories expended.",
    "answer_anchor": "energy imbalance between calories consumed and calories expended"
  },
  {
    "question_id": "Q036",
    "module_id": "2.7",
    "question_type": "risk_factor",
    "question": "What household fuel exposure is highlighted as a major source of harmful household air pollution?",
    "reference_answer": "Cooking or heating with biomass or other solid fuels in the household.",
    "answer_anchor": "cooks with biomass fuel in her household"
  },
  {
    "question_id": "Q037",
    "module_id": "2.7",
    "question_type": "prevention",
    "question": "What practical options does WHO PEN suggest to reduce household air pollution for a person cooking with biomass?",
    "reference_answer": "Switch to cleaner fuels and improve ventilation to reduce exposure.",
    "answer_anchor": "switching to cleaner fuels or reducing HAP, such as by improving ventilation"
  },
  {
    "question_id": "Q038",
    "module_id": "2.7",
    "question_type": "prevention",
    "question": "Which cleaner energy options does WHO PEN mention when advising communities to move away from solid fuels?",
    "reference_answer": "LPG, electricity, solar energy and smokeless stoves.",
    "answer_anchor": "LPG, electricity, solar and smokeless stoves"
  },
  {
    "question_id": "Q039",
    "module_id": "2.7",
    "question_type": "clinical_risk",
    "question": "Which chronic respiratory disease is specifically linked to biomass smoke exposure in the counselling example?",
    "reference_answer": "COPD.",
    "answer_anchor": "predisposes her to frequent cough that can lead to COPD"
  },
  {
    "question_id": "Q040",
    "module_id": "3.1",
    "question_type": "risk_assessment",
    "question": "Which variables are used by the WHO/ISH CVD risk prediction chart shown in WHO PEN?",
    "reference_answer": "Gender, age, systolic blood pressure, total blood cholesterol, smoking status and presence or absence of diabetes mellitus.",
    "answer_anchor": "gender, age, systolic blood pressure, total blood cholesterol, smoking status and presence or absence of diabetes mellitus"
  },
  {
    "question_id": "Q041",
    "module_id": "3.1",
    "question_type": "risk_assessment",
    "question": "What outcome does the WHO/ISH risk prediction chart estimate?",
    "reference_answer": "The 10-year risk of a fatal or non-fatal cardiovascular event.",
    "answer_anchor": "10-year risk of a fatal or non-fatal cardiovascular event"
  },
  {
    "question_id": "Q042",
    "module_id": "3.1",
    "question_type": "risk_assessment",
    "question": "How does WHO PEN describe the result provided by CVD risk prediction charts?",
    "reference_answer": "An approximate combined 10-year risk of developing a heart attack or stroke based on multiple risk factors.",
    "answer_anchor": "It is expressed as a 10-year risk of developing a heart attack or stroke"
  },
  {
    "question_id": "Q043",
    "module_id": "3.1",
    "question_type": "risk_assessment",
    "question": "What method was used to develop the country-specific WHO CVD risk charts?",
    "reference_answer": "Country-specific risk equations were developed from average risk-factor profiles and cardiovascular-event rates in the population.",
    "answer_anchor": "country-specific risk equations based on the average risk factor profile"
  },
  {
    "question_id": "Q044",
    "module_id": "3.1",
    "question_type": "scope",
    "question": "What is the main CVD assessment skill this module is designed to teach primary health-care workers?",
    "reference_answer": "Assessment of 10-year cardiovascular risk using the WHO/ISH risk chart, with early diagnosis, management and timely referral.",
    "answer_anchor": "assess the 10-year risk of cardiovascular diseases"
  },
  {
    "question_id": "Q045",
    "module_id": "3.2",
    "question_type": "screening",
    "question": "Who should be screened for high blood pressure according to WHO PEN?",
    "reference_answer": "All adults should be screened for high blood pressure.",
    "answer_anchor": "All adults should be screened for high BP"
  },
  {
    "question_id": "Q046",
    "module_id": "3.2",
    "question_type": "measurement",
    "question": "How should a patient be positioned and prepared before blood-pressure measurement?",
    "reference_answer": "Sitting with back supported, legs uncrossed, bladder empty, relaxed for five minutes and not talking.",
    "answer_anchor": "back supported, legs uncrossed, bladder empty, relaxed for 5 minutes and not talking"
  },
  {
    "question_id": "Q047",
    "module_id": "3.2",
    "question_type": "measurement",
    "question": "How many BP readings are preferable and how should they be spaced?",
    "reference_answer": "At least two readings, 1–2 minutes apart, using their average.",
    "answer_anchor": "take at least two readings 1–2 minutes apart"
  },
  {
    "question_id": "Q048",
    "module_id": "3.2",
    "question_type": "measurement",
    "question": "At the initial evaluation, what should be done if BP readings differ between the two arms?",
    "reference_answer": "Measure both arms initially and use the arm with the higher reading for subsequent measurements.",
    "answer_anchor": "the arm with the higher reading should be used for measurements thereafter"
  },
  {
    "question_id": "Q049",
    "module_id": "3.2",
    "question_type": "table_numeric",
    "question": "What cuff size is listed for an arm circumference greater than 32 cm?",
    "reference_answer": "Large cuff.",
    "answer_anchor": "use a large cuff if the arm circumference >32 cm"
  },
  {
    "question_id": "Q050",
    "module_id": "3.2",
    "question_type": "diagnostic_criteria",
    "question": "What BP criteria are used to diagnose hypertension on two different visits?",
    "reference_answer": "SBP ≥140 mmHg and/or DBP ≥90 mmHg on both days.",
    "answer_anchor": "SBP on both days is ≥ 140 mmHg and/or DBP is ≥ 90 mmHg"
  },
  {
    "question_id": "Q051",
    "module_id": "3.3",
    "question_type": "symptoms",
    "question": "Which classic symptoms in the WHO PEN diabetes case led the health worker to suspect diabetes?",
    "reference_answer": "Thirst, polyuria and weight loss.",
    "answer_anchor": "thirst, polyuria and weight loss"
  },
  {
    "question_id": "Q052",
    "module_id": "3.3",
    "question_type": "management",
    "question": "What are the first lifestyle principles in managing type 2 diabetes?",
    "reference_answer": "Modify diet and physical activity, and reduce insulin resistance through weight reduction, especially fat-mass reduction.",
    "answer_anchor": "Modify the lifestyle: diet and physical activity"
  },
  {
    "question_id": "Q053",
    "module_id": "3.3",
    "question_type": "pharmacology",
    "question": "Which drug is presented as first-line pharmacological treatment for type 2 diabetes?",
    "reference_answer": "Metformin.",
    "answer_anchor": "Metformin is presented here as the first-line drug"
  },
  {
    "question_id": "Q054",
    "module_id": "3.3",
    "question_type": "numeric",
    "question": "What dose range of metformin is described in WHO PEN?",
    "reference_answer": "250–2000 mg/day.",
    "answer_anchor": "dose of metformin varies from 250 mg to 2000 mg/day"
  },
  {
    "question_id": "Q055",
    "module_id": "3.3",
    "question_type": "treatment_escalation",
    "question": "What does WHO PEN recommend if adequate glucose control is not achieved after increasing metformin to at least 1 g/day?",
    "reference_answer": "Add a sulfonylurea.",
    "answer_anchor": "If despite this dose optimum glucose control is not achieved, a suphonylurea should be added"
  },
  {
    "question_id": "Q056",
    "module_id": "3.4",
    "question_type": "emergency",
    "question": "How does WHO PEN characterize suspected acute stroke?",
    "reference_answer": "Stroke is a medical emergency requiring urgent recognition and referral.",
    "answer_anchor": "Stroke is a medical emergency"
  },
  {
    "question_id": "Q057",
    "module_id": "3.4",
    "question_type": "diagnostics",
    "question": "What imaging tests should be performed as soon as possible in suspected stroke?",
    "reference_answer": "CT or MRI scan.",
    "answer_anchor": "Diagnostic tests (CT/ MRI scan) should be done as soon as possible"
  },
  {
    "question_id": "Q058",
    "module_id": "3.4",
    "question_type": "numeric",
    "question": "Within what time window does WHO PEN say clot-dissolving or clot-treating medicines should be started when indicated and available?",
    "reference_answer": "Within 4.5 hours of stroke onset.",
    "answer_anchor": "started within 4.5 hours"
  },
  {
    "question_id": "Q059",
    "module_id": "3.4",
    "question_type": "rehabilitation",
    "question": "What four main types of therapy are listed for stroke rehabilitation?",
    "reference_answer": "Physical therapy, occupational therapy, speech therapy and emotional-support therapy.",
    "answer_anchor": "The four main types of therapy include"
  },
  {
    "question_id": "Q060",
    "module_id": "3.5",
    "question_type": "etiology",
    "question": "Which bacterial group causing sore throat can lead to rheumatic fever and rheumatic heart disease?",
    "reference_answer": "Group A streptococcus (GAS).",
    "answer_anchor": "Group A streptococcal infections of the throat"
  },
  {
    "question_id": "Q061",
    "module_id": "3.5",
    "question_type": "diagnostic_criteria",
    "question": "When throat culture or rapid testing is unavailable, what McIsaac score prompts antibiotic treatment in WHO PEN?",
    "reference_answer": "A score of 4 or more.",
    "answer_anchor": "If score equals 4 or more then the patient should be treated with antibiotic"
  },
  {
    "question_id": "Q062",
    "module_id": "3.5",
    "question_type": "prophylaxis",
    "question": "How often is intramuscular benzathine benzyl penicillin given for RF/RHD secondary prophylaxis in the listed regimen?",
    "reference_answer": "A single injection once every three weeks.",
    "answer_anchor": "single injection once in three weeks"
  },
  {
    "question_id": "Q063",
    "module_id": "3.5",
    "question_type": "numeric",
    "question": "What benzathine penicillin dose is listed for children under 30 kg?",
    "reference_answer": "600,000 units.",
    "answer_anchor": "for children <30kg: 600 000 units"
  },
  {
    "question_id": "Q064",
    "module_id": "3.5",
    "question_type": "referral",
    "question": "Which RHD patient groups should be referred to secondary or tertiary care?",
    "reference_answer": "Symptomatic RHD, asymptomatic severe valvular disease, and pregnancy in an RHD patient regardless of symptoms.",
    "answer_anchor": "symptomatic RHD"
  },
  {
    "question_id": "Q065",
    "module_id": "3.6",
    "question_type": "differential",
    "question": "Which clinical pattern makes asthma more likely than COPD in WHO PEN?",
    "reference_answer": "Asthma is favored by childhood/early-adult onset, hay fever/eczema/allergies, intermittent symptoms, night/early-morning worsening, triggers and response to salbutamol.",
    "answer_anchor": "symptoms worse at night or early morning"
  },
  {
    "question_id": "Q066",
    "module_id": "3.6",
    "question_type": "differential",
    "question": "Which smoking history is listed as making COPD more likely?",
    "reference_answer": "Heavy smoking of more than 20 cigarettes per day for more than 15 years.",
    "answer_anchor": ">20 cigarettes per day"
  },
  {
    "question_id": "Q067",
    "module_id": "3.6",
    "question_type": "procedure",
    "question": "How is the bronchodilator reversibility test performed with PEFR in the WHO PEN protocol?",
    "reference_answer": "Measure PEFR, give two puffs of salbutamol, then measure PEFR again after 15 minutes.",
    "answer_anchor": "Give two puffs of salbutamol and measure again in 15 minutes"
  },
  {
    "question_id": "Q068",
    "module_id": "3.6",
    "question_type": "diagnostic_criteria",
    "question": "What PEFR improvement after salbutamol makes asthma very probable?",
    "reference_answer": "An improvement of 20% or more.",
    "answer_anchor": "If the PEFR improves by 20%, a diagnosis of asthma is very probable"
  },
  {
    "question_id": "Q069",
    "module_id": "3.6",
    "question_type": "differential",
    "question": "When should tuberculosis be specifically excluded in a patient with chronic cough?",
    "reference_answer": "When there is a history of cough for more than two weeks.",
    "answer_anchor": "tuberculosis must always be excluded when there is a history of cough for more than two weeks"
  },
  {
    "question_id": "Q070",
    "module_id": "3.6",
    "question_type": "acute_management",
    "question": "What are the recommended initial bronchodilators for an acute COPD exacerbation?",
    "reference_answer": "Short-acting inhaled beta2-agonists such as salbutamol, with or without a short-acting anticholinergic such as ipratropium.",
    "answer_anchor": "Short-acting inhaled beta2-agonists, with or without short-acting anticholinergics"
  },
  {
    "question_id": "Q071",
    "module_id": "3.7",
    "question_type": "risk_factor",
    "question": "What major risk factors for oral cancer are emphasized in WHO PEN?",
    "reference_answer": "Tobacco smoking, smokeless tobacco, betel-quid chewing with or without tobacco, excessive alcohol use, and HPV infection for some oral/oropharyngeal cancers.",
    "answer_anchor": "tobacco smoking, smokeless tobacco use"
  },
  {
    "question_id": "Q072",
    "module_id": "3.7",
    "question_type": "screening",
    "question": "What simple examination can frontline workers use to identify oral cancers and potentially malignant lesions?",
    "reference_answer": "A simple visual examination of the mouth, with differentiation from non-cancer lesions.",
    "answer_anchor": "simple, visual examination of the mouth"
  },
  {
    "question_id": "Q073",
    "module_id": "3.7",
    "question_type": "case",
    "question": "In the WHO PEN case of a habitual betel-nut user with white patches and leathery oral changes, what diagnosis is considered?",
    "reference_answer": "Probable oral submucous fibrosis.",
    "answer_anchor": "Probable submucous fibrosis"
  },
  {
    "question_id": "Q074",
    "module_id": "3.7",
    "question_type": "referral",
    "question": "What management is advised for probable oral submucous fibrosis in the case example?",
    "reference_answer": "Tobacco-cessation counselling using the 5A's, mouth-opening exercises, diet counselling and referral for further evaluation.",
    "answer_anchor": "arrange a referral for further evaluation"
  },
  {
    "question_id": "Q075",
    "module_id": "3.8",
    "question_type": "signs",
    "question": "Which breast findings are shown as possible signs of breast cancer in WHO PEN?",
    "reference_answer": "Lump, depression, erythema, peau d'orange, recent nipple retraction, nipple scaliness, nipple discharge and ulceration.",
    "answer_anchor": "peau d’orange"
  },
  {
    "question_id": "Q076",
    "module_id": "3.8",
    "question_type": "referral",
    "question": "Which persistent breast findings require immediate referral for imaging and/or tissue sampling?",
    "reference_answer": "A breast lump with relevant risk factors, an enlarging/fixed/hard lump, or other suspicious findings such as nipple retraction, peau d'orange, ulceration, unilateral particularly bloody discharge, or axillary lump.",
    "answer_anchor": "Refer immediately to a next level health facility"
  },
  {
    "question_id": "Q077",
    "module_id": "3.8",
    "question_type": "screening",
    "question": "What is a clinical breast examination (CBE)?",
    "reference_answer": "Examination of both breasts by a trained health professional, usable diagnostically for a lump or as part of a screening programme.",
    "answer_anchor": "examination of both breasts performed by a trained health professional"
  },
  {
    "question_id": "Q078",
    "module_id": "3.8",
    "question_type": "screening",
    "question": "For which age group does WHO describe organized population-based mammography screening in well-resourced settings, if programme conditions are met?",
    "reference_answer": "Women aged 50–69 years.",
    "answer_anchor": "women aged 50–69 should undergo organized, population-based mammography screening"
  },
  {
    "question_id": "Q079",
    "module_id": "3.8",
    "question_type": "screening",
    "question": "What does WHO PEN say about breast self-examination as a screening method?",
    "reference_answer": "There is no evidence for screening benefit from breast self-examination, but breast awareness is recommended to improve early diagnosis among women at risk.",
    "answer_anchor": "There is no evidence on the effect of screening through breast self-examination"
  },
  {
    "question_id": "Q080",
    "module_id": "3.9",
    "question_type": "prevention",
    "question": "What two main prevention approaches for cervical cancer are highlighted in WHO PEN?",
    "reference_answer": "HPV vaccination and screening.",
    "answer_anchor": "preventable through vaccination and screening"
  },
  {
    "question_id": "Q081",
    "module_id": "3.9",
    "question_type": "risk_factor",
    "question": "How does having many sexual partners relate to cervical-cancer risk according to the module?",
    "reference_answer": "Women with many sexual partners are at higher risk of HPV infection.",
    "answer_anchor": "Women with many sexual partners are at higher risk of HPV infection"
  },
  {
    "question_id": "Q082",
    "module_id": "3.9",
    "question_type": "symptoms",
    "question": "Which bleeding symptom in the case story should raise concern for cervical cancer?",
    "reference_answer": "Post-coital bleeding, especially when persistent or accompanied by abnormal/heavy bleeding.",
    "answer_anchor": "post-coital bleeding"
  },
  {
    "question_id": "Q083",
    "module_id": "3.9",
    "question_type": "procedure",
    "question": "What steps are listed in the speculum-examination competency check?",
    "reference_answer": "Position the model/patient, select the speculum, expose the cervix, fix the speculum blades, then withdraw and clean the speculum.",
    "answer_anchor": "Selection of the speculum"
  },
  {
    "question_id": "Q084",
    "module_id": "3.9",
    "question_type": "referral",
    "question": "Why is early referral of women with suspected cervical cancer emphasized?",
    "reference_answer": "Because cervical cancer can be curable when diagnosed early, and early diagnosis/referral improves survival.",
    "answer_anchor": "refer them early"
  },
  {
    "question_id": "Q085",
    "module_id": "4.1",
    "question_type": "definition",
    "question": "How does WHO PEN define comorbidity in the mental-health and NCD module?",
    "reference_answer": "Mental illness occurring together or coexisting with physical illness.",
    "answer_anchor": "Mental illness occurring together or coexisting with physical illness is referred to as comorbidity"
  },
  {
    "question_id": "Q086",
    "module_id": "4.1",
    "question_type": "clinical_fact",
    "question": "Which mental-health conditions are listed as commonly co-occurring with NCDs?",
    "reference_answer": "Examples include alcohol and tobacco abuse/dependence, depression, anxiety disorders, trauma/stress-related disorders, insomnia, suicide and dementia.",
    "answer_anchor": "depression, anxiety disorders"
  },
  {
    "question_id": "Q087",
    "module_id": "4.1",
    "question_type": "epidemiology",
    "question": "How high does WHO PEN say major-depression prevalence may be among people with cancer?",
    "reference_answer": "Up to 33%, compared with up to 10% in the general population.",
    "answer_anchor": "up to 33% with cancer"
  },
  {
    "question_id": "Q088",
    "module_id": "4.1",
    "question_type": "clinical_reasoning",
    "question": "Does sadness or worry in a patient with an NCD automatically mean depression or anxiety disorder?",
    "reference_answer": "No. Distress can cause sadness and worry, but not all such symptoms reach the level of a psychiatric disorder.",
    "answer_anchor": "Not all sadness or worry is depression and anxiety"
  },
  {
    "question_id": "Q089",
    "module_id": "4.2",
    "question_type": "definition",
    "question": "How is palliative care defined in WHO PEN?",
    "reference_answer": "An approach that improves quality of life for patients and families facing life-threatening illness through prevention and relief of suffering, with early identification, assessment and treatment of physical, psychosocial and spiritual problems.",
    "answer_anchor": "improves the quality of life of patients and their families"
  },
  {
    "question_id": "Q090",
    "module_id": "4.2",
    "question_type": "pain_assessment",
    "question": "What is the single most reliable indicator of pain according to WHO PEN?",
    "reference_answer": "The patient's self-report of pain.",
    "answer_anchor": "patient’s self-report of pain is the single most reliable indicator"
  },
  {
    "question_id": "Q091",
    "module_id": "4.2",
    "question_type": "pain_assessment",
    "question": "Why are unidimensional pain scales suitable for busy clinical settings?",
    "reference_answer": "They assess overall pain intensity and take little time to administer.",
    "answer_anchor": "Unidimensional scales assess the overall intensity of pain"
  },
  {
    "question_id": "Q092",
    "module_id": "4.2",
    "question_type": "pain_management",
    "question": "What are the three core administration principles of the WHO analgesic ladder described in the module?",
    "reference_answer": "By mouth, by the clock, and by the ladder.",
    "answer_anchor": "by the clock"
  },
  {
    "question_id": "Q093",
    "module_id": "4.2",
    "question_type": "pharmacology",
    "question": "Which strong opioid does WHO identify as the opioid of choice for cancer-pain management?",
    "reference_answer": "Morphine.",
    "answer_anchor": "Morphine is WHO’s strong opioid of choice for cancer pain management"
  },
  {
    "question_id": "Q094",
    "module_id": "5.1",
    "question_type": "service_delivery",
    "question": "What is the purpose of PEN peer coaching?",
    "reference_answer": "To build learning primary-health-care teams at the health facility that provide person-centred essential care for major NCDs.",
    "answer_anchor": "Build learning primary healthcare teams"
  },
  {
    "question_id": "Q095",
    "module_id": "5.1",
    "question_type": "framework",
    "question": "What are the three principles of PEN peer coaching?",
    "reference_answer": "Primary health facility-led, primary health facility-driven, and primary health facility-empowered.",
    "answer_anchor": "Primary health facility-led"
  },
  {
    "question_id": "Q096",
    "module_id": "5.1",
    "question_type": "framework",
    "question": "What are the four components of the PEN peer-coaching PIDI cycle?",
    "reference_answer": "Plan and prepare for coaching, implement coaching, deliver PEN services to clients, and improve practices.",
    "answer_anchor": "Plan and prepare for coaching"
  },
  {
    "question_id": "Q097",
    "module_id": "5.1",
    "question_type": "quality_improvement",
    "question": "How does WHO PEN define a clinical audit?",
    "reference_answer": "A continuous quality-improvement process that measures current patient care and outcomes against explicit agreed standards or audit criteria.",
    "answer_anchor": "Clinical audit is a quality improvement tool"
  },
  {
    "question_id": "Q098",
    "module_id": "5.2",
    "question_type": "definition",
    "question": "How does WHO PEN define monitoring?",
    "reference_answer": "The ongoing collection, management and use of information to assess whether an activity or programme is proceeding according to plan and/or achieving defined targets.",
    "answer_anchor": "Monitoring is the ongoing collection, management and use of information"
  },
  {
    "question_id": "Q099",
    "module_id": "5.2",
    "question_type": "purpose",
    "question": "What is the purpose of the PEN monitoring system?",
    "reference_answer": "To support continuous improvement of services by assessing performance of the PHC service-delivery system.",
    "answer_anchor": "purpose of a PEN monitoring system is to support continuous improvement of services"
  },
  {
    "question_id": "Q100",
    "module_id": "5.2",
    "question_type": "monitoring",
    "question": "What does WHO PEN describe as the foundation of a monitoring system?",
    "reference_answer": "Indicators.",
    "answer_anchor": "Indicators are the foundation of a monitoring system"
  }
]

assert len(GOLD_100_CANDIDATES) == 100
assert len({x["question_id"] for x in GOLD_100_CANDIDATES}) == 100

def gold_norm(text: str) -> str:
    text = normalize_medical_text(str(text or ""))
    text = text.replace("’", "'")
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

_gold_leaves = leaves_df.copy()
_gold_leaves["_gold_text"] = _gold_leaves["text"].astype(str).map(gold_norm)

resolved = []
unresolved = []

for case in GOLD_100_CANDIDATES:
    module_mask = _gold_leaves["module_id"].astype(str).eq(str(case["module_id"]))
    needle = gold_norm(case["answer_anchor"])

    matches = _gold_leaves[
        module_mask &
        _gold_leaves["_gold_text"].str.contains(re.escape(needle), regex=True, na=False)
    ].copy()

    if matches.empty:
        unresolved.append(case)
        continue

    relevant_leaf_ids = matches["leaf_id"].astype(str).drop_duplicates().tolist()
    relevant_parent_ids = matches["parent_id"].astype(str).drop_duplicates().tolist()

    resolved.append({
        "question_id": case["question_id"],
        "module_id": case["module_id"],
        "question_type": case["question_type"],
        "question": case["question"],
        "relevant_leaf_ids": relevant_leaf_ids,
        "relevant_parent_ids": relevant_parent_ids,
        "reference_answer": case["reference_answer"],
        "answer_anchor": case["answer_anchor"],
        "notes": (
            "Source-grounded anchor automatically resolved in corrected leaves. "
            "Clinician review is still required before final production acceptance."
        ),
    })

gold100_df = pd.DataFrame(resolved)
unresolved_df = pd.DataFrame(unresolved)

print("=" * 90)
print("WHO PEN GOLD-100 SOURCE ANCHOR VALIDATION")
print("=" * 90)
print("Candidates :", len(GOLD_100_CANDIDATES))
print("Resolved   :", len(gold100_df))
print("Unresolved :", len(unresolved_df))
print("Coverage   :", f"{len(gold100_df) / 100:.1%}")

if len(unresolved_df):
    print("\nUNRESOLVED CASES:")
    print(
        unresolved_df[
            ["question_id", "module_id", "question", "answer_anchor"]
        ].to_string(index=False)
    )

GOLD100_PATH = CFG.root / "eval" / "human_gold_100_source_grounded.jsonl"
GOLD100_PATH.parent.mkdir(parents=True, exist_ok=True)

with GOLD100_PATH.open("w", encoding="utf-8") as f:
    for row in resolved:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("\nSaved:", GOLD100_PATH)

if len(gold100_df):
    module_counts = (
        gold100_df.groupby("module_id")
        .size()
        .rename("questions")
        .reset_index()
    )
    display(module_counts)
    display(gold100_df.head(10))

if len(unresolved_df) == 0:
    print("\n✅ ALL 100 source anchors resolved to exact leaf evidence.")
    print("➡️ Next: run Cell 47B formal deterministic retrieval metrics.")
else:
    print("\n⚠️ Do NOT run the formal 100-question metrics yet.")
    print("➡️ Send me the unresolved table; we will fix only those anchors.")
