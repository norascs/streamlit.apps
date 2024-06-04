import streamlit as st
import openai

openai.api_key = ''

def generate_grad_admission_recommendation(field, interests, favorite_class, additional_questions):
    """
    Generates in-depth recommendations for grad school admission based on the user's field of interest,
    subjects they are most interested in, their favorite class, and answers to other relevant questions.
    """
    prompt = f"""
    Provide a detailed recommendation for a student interested in graduate studies in the following:
    - Field of interest: {field}
    - Subjects of interest within the field: {interests}
    - Favorite class and why it was favored: {favorite_class}
    - Additional details that might help in personalizing recommendations: {additional_questions}
    
    The recommendation should include:
    - Names of suitable graduate programs and universities.
    - Specific professors at these institutions who are experts in the subjects of interest, including a brief overview of their research focus.
    - Links to the department or program websites for more information.
    - Any additional resources or advice that would be beneficial for a prospective graduate student in this field.
    """
    
    system_message = """
    You are a highly knowledgeable assistant specialized in providing comprehensive and personalized recommendations for students seeking graduate education. Your responses should be detailed, including the names of specific programs and universities, notable faculty members and their areas of expertise, direct links to relevant department or program websites, and any useful additional resources or advice. Aim to assist the user in making informed decisions about their graduate studies path.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message},
                      {"role": "user", "content": prompt}],
            max_tokens=2000  # Increased token limit to allow for more detailed responses
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return str(e)

def generate_post_graduation_plan(major, fields_of_interest, additional_details):
    """
    Generates suggestions for what to do after graduation based on the user's major, fields of interest, and any additional details they provide.
    """
    prompt = f"""
    Given a student with a major in {major} who is interested in fields such as {fields_of_interest}, along with the following additional details: {additional_details}, provide a comprehensive plan for what they could consider doing after graduation. This plan should include potential career paths, further education opportunities, training programs, and any other recommendations that would help them advance in their desired fields.
    """
    
    system_message = """
    You are a knowledgeable assistant specialized in career and educational guidance. Your task is to provide a detailed and actionable plan for students wondering what to do after their graduation. This plan should be tailored to the student's specific major, their fields of interest, and any additional information they have provided. Ensure the plan includes a variety of options such as career paths, further education, training programs, and any other relevant opportunities. Aim to assist the user in making informed decisions about their future.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message},
                      {"role": "user", "content": prompt}],
            max_tokens=500  # Adjust based on your needs
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return str(e)

# Streamlit app layout with tabs
st.title('NC Path Finder')

tab1, tab2 = st.tabs(["Grad Admission Field Discoverer", "What to Do After Graduation"])

with tab1:
    st.header("Grad Discovery")
    st.subheader("Press the submit button once and wait.")

    # User inputs for grad admission recommendations
    field = st.text_input("Field of interest")
    interests = st.text_input("Subjects of interest within the field")
    favorite_class = st.text_input("Favorite class and why")
    additional_questions = st.text_area("Any additional details?")
    
    if st.button('Submit for Recommendations'):
        recommendations = generate_grad_admission_recommendation(field, interests, favorite_class, additional_questions)
        st.text_area("Recommendations", recommendations, height=250)

with tab2:
    st.header("After Graduation Plan")
    st.subheader("Press the submit button once and wait.")

    # User inputs for post-graduation planning
    major = st.text_input("Your Major")
    fields_of_interest = st.text_input("Fields you want to go into")
    additional_details = st.text_area("Any additional details or considerations?")
    
    if st.button('Submit for Post-Graduation Plan'):
        plan = generate_post_graduation_plan(major, fields_of_interest, additional_details)
        st.text_area("Your Post-Graduation Plan", plan, height=250)
