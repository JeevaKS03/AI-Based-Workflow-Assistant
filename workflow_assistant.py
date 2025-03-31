import streamlit as st
import PyPDF2  
import docx 
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url="SERVER_URL",
    api_key="API_KEY"
)
model_id = "ibm/granite-13b-instruct-v2"
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 200,
    "min_new_tokens": 0,
    "repetition_penalty": 1
}
project_id = "PROJECT_ID"

model = ModelInference(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=project_id
)

st.set_page_config(page_title="AI Assistant", layout="wide")
st.title("Workflow Assistant")

tabs = ["Generate Email", "Generate Tasks", "Document Upload", "Meeting Transcript"]
selected_tab = st.radio("Select a tab", tabs)

def extract_text_from_pdf(uploaded_file):
    text = ""
    with PyPDF2.PdfReader(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

if selected_tab == "Document Upload":
    st.subheader("Upload a Document")
    
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            st.write("Extracting text from PDF...")
            text = extract_text_from_pdf(uploaded_file)
            st.text_area("Extracted Text from PDF", text, height=300)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            st.write("Extracting text from DOCX...")
            text = extract_text_from_docx(uploaded_file)
            st.text_area("Extracted Text from DOCX", text, height=300)
        else:
            st.error("Unsupported file type. Please upload a PDF or DOCX file.")
        prompt_input = f"""Document Content: The company reported a 15% increase in revenue for Q1 2025 compared to the previous year, driven by strong sales in the North American and European markets. However, operating costs also rose by 8% due to higher logistics expenses. The management has decided to invest in AI-driven supply chain optimization to reduce future costs. Additionally, the company plans to expand its product line to include smart home devices, expecting a 20% growth in revenue by next year.
Summary: Q1 2025 revenue grew by 15% due to strong North American and European sales. Operating costs increased by 8% due to logistics. The company plans AI-driven supply chain improvements and smart home product expansion for 20% future growth.

Document Content: John has consistently met project deadlines and demonstrated strong problem-solving skills. He collaborates effectively with his team and takes initiative in improving workflows. However, he needs to improve time management, as he occasionally struggles with prioritizing tasks. Overall, he is a valuable asset to the team and has shown great potential for a leadership role.
Summary: John is a reliable team player who meets deadlines and solves problems effectively. He takes initiative and collaborates well, though time management needs improvement. He has leadership potential

Document Content: The team discussed the upcoming project deadline and assigned tasks accordingly. The marketing team will handle outreach, while the development team will finalize the product features. The finance team will allocate the necessary budget. A follow-up meeting is scheduled for next Monday to review progress and resolve any roadblocks.
Summary: Project tasks assigned: marketing (outreach), development (finalizing features), and finance (budget allocation). Follow-up meeting next Monday

Document Content: The company has introduced a new remote work policy allowing employees to work from home up to three days a week. Employees must ensure availability during core working hours and maintain productivity. Managers will review requests for exceptions on a case-by-case basis. Additionally, a reimbursement plan for home office equipment has been implemented, with a cap of $500 per employee.
Summary: New remote work policy: up to 3 days/week, availability required during core hours. $500 reimbursement for home office setup. Exceptions reviewed by managers.

Document Content: New employees must complete onboarding within their first two weeks. This includes HR paperwork, IT system setup, and team introductions. They are assigned a mentor for guidance. Performance goals will be set in the first month, with a 3-month review meeting scheduled to assess progress.
Summary: Onboarding: complete paperwork, IT setup, and meet the team in 2 weeks. Mentors assigned. Performance goals set in 1st month, review after 3 months.

Document Content: The recent cybersecurity training covered best practices for password management, phishing attack prevention, and secure data handling. Employees were required to complete an assessment, with an 85% passing rate. Future training sessions will focus on advanced security protocols. Feedback from employees highlighted the need for more hands-on exercises.
Summary: Cybersecurity training: covered passwords, phishing prevention, and data security. 85% pass rate. Future sessions will focus on advanced protocols. Employees request more hands-on exercises.

Document Content: {text}
Summary:"""    
        if st.button("Generate",key="document"):
             st.write("Submitting generation request...")
             generated_response = model.generate_text(prompt=prompt_input, guardrails=False)
             st.write(generated_response)    

    
elif selected_tab == "Generate Email":
    input_text = st.text_area("Enter the prompt for Generating Email:")
    prompt_input = f"""Input: Recipient: Manager
Subject: Project Discussion
Greeting: Formal
Purpose: Request a meeting to discuss project progress
Key Points:
Update on current status
Roadblocks and solutions
Next steps and deadlines
Action Required: Confirm availability for a meeting
Closing Note: Looking forward to your response
Signature: John Doe, Project Lead
Output: Subject: Request for Project Discussion Meeting
Dear [Manager's Name],
I hope you are doing well. I would like to request a meeting to discuss the current progress of our project.
Key discussion points include:
An update on the current status
Roadblocks faced and potential solutions
Next steps and upcoming deadlines
Please let me know your availability for a brief discussion at your convenience. Looking forward to your response.
Best regards,
John Doe
Project Lead

Input: Recipient: Accounts Team
Subject: Pending Invoice Payment
Greeting: Formal
Purpose: Follow-up on unpaid invoice
Key Points:
Invoice #12345 due on March 25
Amount: $5,000
Payment not received yet
Action Required: Confirm payment status or expected date
Closing Note: Appreciate your prompt response
Signature: Jane Smith, Finance Department
Output: Subject: Follow-up on Pending Invoice Payment
Dear Accounts Team,
I hope this email finds you well. I am reaching out to follow up on the pending payment for Invoice #12345, which was due on March 25. As of today, we have not received the payment of $5,000.
Could you kindly confirm the payment status or provide an estimated date for processing? Your prompt response would be greatly appreciated.
Best regards,
Jane Smith
Finance Department

Input: Recipient: HR Manager
Subject: Job Application – Software Engineer Position
Greeting: Formal
Purpose: Apply for a job opening
Key Points:
Applying for Software Engineer role
Attached resume and portfolio
Available for interview at convenience
Action Required: Review application and schedule interview
Closing Note: Looking forward to the opportunity
Signature: Michael Brown, Software Developer
Output: Subject: Application for Software Engineer Position
Dear [HR Manager's Name],
I hope you are doing well. I am writing to express my interest in the Software Engineer position at [Company Name]. Please find my resume and portfolio attached for your review.
I would love the opportunity to discuss how my skills align with the role. Kindly let me know if we can schedule an interview at your convenience. Looking forward to your response.
Best regards,
Michael Brown
Software Developer


Input: Recipient: Team Lead
Subject: Leave Request for April 10-12
Greeting: Formal
Purpose: Request time off
Key Points:
Need leave from April 10-12
Reason: Family commitment
Work handover plan included
Action Required: Approve leave request
Closing Note: Appreciate your support
Signature: Sarah Johnson, Marketing Executive
Output: Subject: Request for Leave (April 10-12)
Dear [Team Lead's Name],
I hope you are doing well. I would like to request leave from April 10 to April 12 due to a family commitment. I have ensured that all pending tasks are completed, and I have coordinated with [Colleague’s Name] for any urgent matters during my absence.
Please let me know if you require any further details. I appreciate your support and look forward to your approval.
Best regards,
Sarah Johnson
Marketing Executive


Input: Recipient: Sales Team
Subject: Inquiry About Product Availability
Greeting: Formal
Purpose: Ask about stock availability and pricing
Key Points:
Interested in purchasing Model X123
Need bulk order details and delivery timeline
Requesting a price quote
Action Required: Provide product details and pricing
Closing Note: Looking forward to your response
Signature: David Lee, Procurement Manager
Output: Subject: Inquiry About Product Availability – Model X123
Dear Sales Team,
I hope you are doing well. I am interested in purchasing Model X123 in bulk and would like to inquire about its availability, pricing, and delivery timeline.
Could you please provide a price quote and any applicable bulk order discounts? Looking forward to your response at your earliest convenience.
Best regards,
David Lee
Procurement Manager

Input: {input_text}
Output:"""
    
elif selected_tab == "Generate Tasks":
    input_text = st.text_area("Enter the Tasks for Prioritizing:")
    prompt_input = f"""Tasks: Client meeting at 9 AM (1.5 hrs)
Submit project report before 12 PM
Review team progress before 2 PM
Code debugging before 5 PM
Follow up with vendor before 7 PM
Priority Order: 1. Client meeting – Fixed time, cannot be postponed.
2. Submit project report – Deadline before noon, high importance.
3. Review team progress – Important for workflow but can be adjusted.
4. Code debugging – Necessary but not urgent.
5. Follow up with vendor – Can be done anytime before 7 PM.


Tasks: Respond to emails before 10 AM
Complete documentation before 12 PM
Team stand-up meeting at 2 PM (30 min)
Work on UI design before 4 PM
Update stakeholders before 6 PM
Priority Order: 1. Respond to emails – Essential for communication.
2. Complete documentation – Has a deadline before noon.
3. Team stand-up meeting – Fixed time, required for coordination.
4. Update stakeholders – Needs to be done but not as urgent.
5. Work on UI design – Creative work can be scheduled flexibly.


Tasks: Prepare presentation before 11 AM
Check financial reports before 1 PM
Finalize marketing strategy before 3 PM
Approve new project proposals before 5 PM
Assign new tasks to team before 7 PM
Priority Order: 1. Prepare presentation – Has an early deadline.
2. Check financial reports – Needed for decision-making.
3. Finalize marketing strategy – Must be done before the meeting.
4. Approve new project proposals – Important but can be done later.
5. Assign new tasks to team – Can be the last task of the day.

Tasks: Fix login bug before 11 AM
Review pull requests before 1 PM
Implement new API before 3 PM
Test application before 5 PM
Deploy new update before 8 PM
Priority Order: 1. Fix login bug – Critical for users, high urgency.
2. Review pull requests – Needed for team workflow.
3. Implement new API – Time-consuming but important.
4. Test application – Required before deployment.
5. Deploy new update – Final step after testing.

Tasks: Write blog post before 10 AM
Edit client’s video before 1 PM
Send invoices before 3 PM
Work on website redesign before 6 PM
Schedule social media posts before 9 PM
Priority Order: 1. Edit client’s video – Paid work, needs to be delivered.
2. Send Invoices – Important for getting paid.
3. Write blog post – Less urgent but has a deadline.
4. Work on website redesign – Flexible timing.
5. Schedule social media posts – Can be automated.

Tasks: Call with investors at 10 AM (1 hr)
Analyze sales report before 12 PM
Develop new business strategy before 2 PM
Interview potential hires before 4 PM
Finalize next quarter plans before 7 PM
Priority Order: 1. Call with investors – Fixed time, crucial.
2. Analyze sales report – Needed for strategic planning.
3. Develop new business strategy – High impact.
4. Interview potential hires – Can be rescheduled if needed.
5. Finalize next quarter plans – Last but essential.

Tasks: Attend morning briefing at 8 AM
Check patient reports before 11 AM
Perform scheduled surgeries before 3 PM
Follow up with patients before 6 PM
Document case studies before 9 PM
Priority Order: 1. Attend morning briefing – Essential for coordination.
2. Perform scheduled surgeries – High priority, critical.
3. Check patient reports – Helps in decision-making.
4. Follow up with patients – Important but flexible.
5. Document case studies – Can be done at the end.


Tasks: Revise math notes before 10 AM
Complete assignment before 12 PM
Attend online lecture at 2 PM (1.5 hrs)
Practice coding problems before 5 PM
Prepare for tomorrow’s quiz before 8 PM
Priority Order: 1. Complete assignment – Submission deadline is close.
2. Attend online lecture – Fixed schedule.
3. Revise math notes – Helps in understanding concepts.
4. Prepare for tomorrow’s quiz – Important but later in the day.
5. Practice coding problems – Can be done anytime.

Tasks: Brainstorm video ideas before 10 AM
Script writing before 12 PM
Film content before 3 PM
Edit and finalize video before 6 PM
Schedule uploads and promotions before 9 PM
Priority Order: 1. Script writing – Foundation for content.
2. Film content – Needs time and setup.
3. Edit and finalize video – Time-consuming but necessary.
4. Schedule uploads – Last step of the process.
5. Brainstorm video ideas – Can be done flexibly.

Tasks: Confirm venue bookings before 10 AM
Arrange catering before 12 PM
Finalize guest list before 2 PM
Set up event space before 5 PM
Oversee event execution before 9 PM
Priority Order: 1. Confirm venue bookings – Must be done first.
2. Arrange catering – Crucial for event planning.
3. Finalize guest list – Needed before invitations go out.
4. Set up event space – Important but can be done later.
5. Oversee event execution – The final step.

Tasks:{input_text}
Priority Order:"""

elif selected_tab == "Meeting Transcript":
    input_text = st.text_area("Enter the meeting transcript:")
    if input_text:
        prompt_input = f"""Write a short summary for the meeting transcripts.

Transcript: 00:00   [John]   I wanted to share an update on project X today.
00:15   [John]   Project X will be completed at the end of the week.
00:30   [Jane]  That's great!
00:35   [Jane]  I heard from customer Y today, and they agreed to buy our product.
00:45   [Joe]  Customer Z said they will too.
01:05   [John]   Great news, all around.
Summary: John shared an update that project X will be completed end of the week and will be purchased by customers Y and Z.

Transcript: 00:00   [Jane]   The goal today is to agree on a design solution.
00:12   [John]  I think we should consider choice 1.
00:25   [Jane]   I agree
00:40   [Joe]  Choice 2 has the advantage that it will take less time.
01:03   [John]  Actually, that's a good point.
01:30   [Jane]   So, what should we do?
01:55   [John]  I'm good with choice 2.
02:20   [Joe]  Me too.
02:45   [Jane] Done!
Summary: Jane, John, and Joe decided to go with choice 2 for the design solution because it will take less time.

Transcript: 00:00 [Sarah] Let’s kick off the meeting for Project Alpha.
00:10 [Mark] I’ve assigned the design team to start on the UI this week.
00:25 [Sarah] Great. What’s the timeline for the first prototype?
00:40 [Mark] We’re aiming for two weeks from now.
01:00 [Lisa] I’ll coordinate with the dev team to align backend work.
Summary: Sarah and Mark kicked off Project Alpha, with the design team starting on the UI this week. The first prototype is expected in two weeks, and Lisa will coordinate with the dev team for backend alignment.

Transcript: 00:00 [John] I met with Client B yesterday about their feedback.
00:15 [Emma] What did they say about the new feature?
00:30 [John] They liked it but want faster load times.
00:45 [Emma] Okay, I’ll prioritize that with the team.
01:00 [John] They also requested a demo next week.
Summary: John shared Client B’s feedback, noting they liked the new feature but want faster load times, which Emma will prioritize. The client also requested a demo next week.

Transcript: 00:00 [Tom] Let’s review the Q1 budget for the marketing team.
00:20 [Anna] We’ve spent 60% of the budget so far.
00:35 [Tom] That’s higher than expected. Any concerns?
00:50 [Anna] Yes, the ad campaign costs were higher due to last-minute changes.
01:10 [Tom] Let’s adjust for Q2 and reduce ad spend.
Summary: Tom and Anna reviewed the Q1 marketing budget, noting 60% has been spent, largely due to high ad campaign costs. They agreed to adjust and reduce ad spend in Q2.

Transcript: 00:00 [Rachel] We’re planning the launch for Product X next month.
00:15 [Mike] The marketing team is ready with the campaign.
00:30 [Rachel] Good. What about the sales team?
00:45 [Mike] They’re training this week to prepare.
01:00 [Rachel] Let’s schedule a dry run next Friday.
Summary: Rachel and Mike discussed the Product X launch next month. The marketing team is ready, the sales team is in training, and a dry run is scheduled for next Friday.

Transcript: 00:00 [David] Let’s go over the team’s performance this quarter.
00:10 [Sophie] The dev team exceeded their sprint goals.
00:25 [David] That’s excellent. Any challenges?
00:40 [Sophie] Yes, the QA team needs more resources.
00:55 [David] I’ll approve hiring two more QA engineers.
Summary: David and Sophie reviewed the team’s performance, noting the dev team exceeded goals. The QA team needs more resources, so David approved hiring two more QA engineers.

Transcript: 00:00 [Emily] I spoke with Vendor Y about the contract terms.
00:15 [Chris] Did they agree to the pricing we proposed?
00:30 [Emily] Not yet, but they’re open to a 5% discount.
00:45 [Chris] That’s a start. Let’s push for 10%.
01:00 [Emily] I’ll follow up tomorrow.
Summary: Emily updated Chris on Vendor Y’s contract terms, noting they offered a 5% discount. Chris suggested pushing for 10%, and Emily will follow up tomorrow.

Transcript: 00:00 [Alex] Let’s plan the next sprint for the dev team.
00:15 [Nina] We have 10 user stories to prioritize.
00:30 [Alex] Let’s focus on the payment feature first.
00:45 [Nina] Agreed. We’ll allocate three developers to it.
01:00 [Alex] Sounds good. Let’s review progress next week.
Summary: Alex and Nina planned the next sprint, prioritizing the payment feature with three developers assigned. They’ll review progress next week.

Transcript: 00:00 [Laura] I have an update on customer support tickets.
00:20 [Ben] How many are unresolved?
00:35 [Laura] We’re down to 50 from 200 last month.
00:50 [Ben] Great progress. Any recurring issues?
01:05 [Laura] Yes, login errors. I’ll escalate to the tech team.
Summary: Laura reported that customer support tickets dropped to 50 from 200, with login errors as a recurring issue to be escalated to the tech team, as discussed with Ben.

Transcript: {input_text}
Summary:"""

if st.button("Generate"):
    st.write("Submitting generation request...")
    generated_response = model.generate_text(prompt=prompt_input, guardrails=False)
    st.write(generated_response)
