import streamlit as st
import openai
from PIL import Image
import io
import base64
import os
import pandas as pd
import matplotlib.pyplot as plt
import time

OPENAI_API_KEY = ""
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Apply custom styles
st.markdown("""
    <style>
        body {
            background-color: #a64cf7; /* Light purple background */
        }
        .stApp {
            background-color: #a64cf7;
        }
        .uploaded-image {
            display: flex;
            justify-content: center;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #e9d8fa;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            border: none;
        }
        .stTabs [aria-selected="true"] {
            background-color: #d4b9f0;
            border-bottom: 2px solid #8a2be2;
        }
        .battery-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "battery_details" not in st.session_state:
    st.session_state.battery_details = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_enabled" not in st.session_state:
    st.session_state.chat_enabled = False
if "battery_history" not in st.session_state:
    st.session_state.battery_history = []
if "battery_type_counts" not in st.session_state:
    st.session_state.battery_type_counts = {}
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False
if "comparison_data" not in st.session_state:
    # Common battery types comparison data
    st.session_state.comparison_data = {
        'Type': ['Alkaline', 'Lithium', 'NiMH', 'NiCd', 'Lead Acid'],
        'Voltage': [1.5, 3.6, 1.2, 1.2, 2.0],
        'Lifespan (cycles)': [1, 1000, 1000, 500, 300],
        'Energy Density (Wh/kg)': [80, 150, 60, 40, 30],
        'Self-Discharge (% per month)': [2, 1, 30, 20, 5],
        'Cost': ['Low', 'High', 'Medium', 'Medium', 'Low']
    }

# Sidebar navigation
st.sidebar.title("🔋 Battery Hub")
app_mode = st.sidebar.radio("Navigation", ["Home", "Battery Analyzer", "Battery Comparison", "Recycling Info", "Usage History"])

# Function to extract battery type from details
def extract_battery_type(details):
    if not details:
        return "Unknown"
    
    battery_types = ["Alkaline", "Lithium", "NiMH", "Nickel-Metal Hydride", "NiCd", "Nickel-Cadmium", 
                     "Lead Acid", "Li-ion", "Lithium-ion", "Button Cell", "Zinc-Carbon", "Silver Oxide"]
    
    for btype in battery_types:
        if btype.lower() in details.lower():
            return btype
    
    return "Other"

# Function to save battery to history
def save_to_history(image, details):
    # Extract key info
    battery_type = extract_battery_type(details)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Convert image to base64 for storage
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Add to history
    st.session_state.battery_history.append({
        "timestamp": timestamp,
        "type": battery_type,
        "details": details,
        "image": img_str
    })
    
    # Update type counts for statistics
    if battery_type in st.session_state.battery_type_counts:
        st.session_state.battery_type_counts[battery_type] += 1
    else:
        st.session_state.battery_type_counts[battery_type] = 1

# HOME PAGE
if app_mode == "Home":
    st.title("🔋 Battery Hub: One Spot for Batteries!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to Battery Hub!
        
        Your intelligent assistant for all things battery-related:
        
        - 📸 **Identify batteries** from photos
        - 💬 **Chat with our AI** about battery specs and usage
        - 📊 **Compare different battery types**
        - ♻️ **Learn about proper recycling**
        - 📝 **Track your battery usage** over time
        
        Get started by navigating to the Battery Analyzer section!
        """)
    
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=150)
        
        # Quick stats if there's history
        if len(st.session_state.battery_history) > 0:
            st.info(f"You've analyzed {len(st.session_state.battery_history)} batteries so far!")

# BATTERY ANALYZER PAGE
elif app_mode == "Battery Analyzer":
    st.title("🔍 Battery Analyzer")
    st.write("Upload an image of a household battery to analyze it.")

    # Image Upload
    uploaded_file = st.file_uploader("Upload a battery image", type=["jpg", "jpeg", "png"])

    # Display uploaded image in a smaller size
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Battery Image", width=250)

        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Call OpenAI Vision API
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Analyze Battery", key="analyze_btn"):
                with st.spinner("Analyzing battery... This may take a moment."):
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4-turbo",
                            messages=[
                                {"role": "system", "content": """You are an expert in battery analysis. 
                                 Identify the battery and provide details in a structured format with headers:
                                 - Type: (e.g., Alkaline, Lithium-ion, NiMH)
                                 - Voltage: 
                                 - Size/Form Factor:
                                 - Common Uses:
                                 - Approximate Capacity:
                                 - Shelf Life:
                                 - Safety Handling:
                                 - Recycling Instructions:"""},
                                {"role": "user", "content": [
                                    {"type": "text", "text": "Analyze this battery and provide its details."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
                                ]}
                            ],
                            max_tokens=500
                        )

                        # Store battery details in session
                        st.session_state.battery_details = response.choices[0].message.content
                        st.session_state.chat_enabled = True
                        st.session_state.messages = []
                        
                        # Save to history
                        save_to_history(image, st.session_state.battery_details)

                    except Exception as e:
                        st.error(f"Error analyzing the image: {e}")
        
        with col2:
            if st.button("Take Photo (Camera)", key="camera_btn"):
                st.info("Camera functionality would be implemented here. For now, please use the file uploader.")

    # Create tabs for displaying results
    if st.session_state.battery_details:
        tabs = st.tabs(["Battery Details", "Ask Questions", "Feedback"])
        
        # Tab 1: Battery Details
        with tabs[0]:
            st.markdown('<div class="battery-card">', unsafe_allow_html=True)
            st.subheader("🔋 Battery Details")
            st.markdown(st.session_state.battery_details)
            
            # Generate battery replacement suggestions
            battery_type = extract_battery_type(st.session_state.battery_details)
            if battery_type != "Unknown":
                with st.expander("View Compatible Alternatives"):
                    try:
                        alt_response = client.chat.completions.create(
                            model="gpt-4-turbo",
                            messages=[
                                {"role": "system", "content": "You are a battery expert. Provide compatible battery alternatives."},
                                {"role": "user", "content": f"Given this battery info, list 3 compatible alternatives with brief descriptions:\n{st.session_state.battery_details}"}
                            ],
                            max_tokens=300
                        )
                        st.markdown(alt_response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error generating alternatives: {e}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add download option
            if st.download_button(
                label="Download Battery Info (TXT)",
                data=st.session_state.battery_details,
                file_name="battery_analysis.txt",
                mime="text/plain"
            ):
                st.success("Battery information downloaded!")
        
        # Tab 2: Chatbot UI
        with tabs[1]:
            st.subheader("⚡ Power Up Your Knowledge! Ask About This Battery")
            
            # Display chat history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # User Input
            user_query = st.chat_input("Ask something about this battery...")

            if user_query:
                # Add user query to session and immediately display it
                st.session_state.messages.append({"role": "user", "content": user_query})
                
                # Display the new user message immediately
                with st.chat_message("user"):
                    st.write(user_query)

                try:
                    # Get chatbot response
                    chat_response = client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=[
                            {"role": "system", "content": "You are a battery expert. Answer questions based on the provided battery details."},
                            {"role": "assistant", "content": f"Battery details: {st.session_state.battery_details}"},
                            {"role": "user", "content": user_query}
                        ],
                        max_tokens=300
                    )

                    # Extract response
                    bot_reply = chat_response.choices[0].message.content
                    
                    # Add to session and display immediately
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    
                    with st.chat_message("assistant"):
                        st.write(bot_reply)

                except Exception as e:
                    st.error(f"Error processing chatbot response: {e}")
        
        # Tab 3: Feedback
        with tabs[2]:
            st.subheader("💬 Provide Feedback")
            
            if not st.session_state.feedback_given:
                st.write("Was the battery identification accurate?")
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("👍 Yes, accurate"):
                        st.session_state.feedback_given = True
                        st.success("Thanks for your feedback!")
                
                with col2:
                    if st.button("👎 No, inaccurate"):
                        st.session_state.feedback_given = True
                        st.success("Thanks for your feedback! We'll work to improve.")
                
                with col3:
                    if st.button("🤔 Partially correct"):
                        st.session_state.feedback_given = True
                        st.success("Thanks for your feedback!")
                
                feedback_text = st.text_area("Additional comments (optional):")
                if st.button("Submit Feedback"):
                    if feedback_text:
                        st.success("Thank you for your detailed feedback!")
                        st.session_state.feedback_given = True
            else:
                st.success("Thank you for your feedback!")

# BATTERY COMPARISON PAGE
elif app_mode == "Battery Comparison":
    st.title("📊 Battery Type Comparison")
    
    # Create a DataFrame
    df = pd.DataFrame(st.session_state.comparison_data)
    
    # Display as table
    st.subheader("Battery Types Comparison Table")
    st.dataframe(df.set_index('Type'))
    
    # Create comparison charts
    st.subheader("Battery Performance Metrics")
    
    chart_option = st.selectbox(
        "Select comparison metric:", 
        ["Voltage", "Lifespan (cycles)", "Energy Density (Wh/kg)", "Self-Discharge (% per month)"]
    )
    
    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Only use numeric columns for the chart
    if chart_option in df.columns and df[chart_option].dtype != 'object':
        ax.bar(df['Type'], df[chart_option], color='purple')
        ax.set_title(f'Comparison of {chart_option} by Battery Type')
        ax.set_ylabel(chart_option)
        ax.set_xlabel('Battery Type')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
    
    # Additional comparison features
    st.subheader("Custom Battery Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        battery1 = st.selectbox("Select first battery type:", df['Type'])
    
    with col2:
        battery2 = st.selectbox("Select second battery type:", df['Type'], index=1)
    
    if st.button("Compare Selected Batteries"):
        # Filter data for selected batteries
        b1_data = df[df['Type'] == battery1].iloc[0]
        b2_data = df[df['Type'] == battery2].iloc[0]
        
        # Create comparison
        comparison = pd.DataFrame({
            'Metric': df.columns[1:],  # Skip the 'Type' column
            battery1: b1_data[1:],
            battery2: b2_data[1:]
        })
        
        st.table(comparison.set_index('Metric'))
        
        # Generate detailed comparison
        st.subheader("Detailed Comparison Analysis")
        
        try:
            comparison_prompt = f"""
            Compare these two battery types in detail:
            
            {battery1}: 
            Voltage: {b1_data['Voltage']}
            Lifespan: {b1_data['Lifespan (cycles)']} cycles
            Energy Density: {b1_data['Energy Density (Wh/kg)']} Wh/kg
            Self-Discharge: {b1_data['Self-Discharge (% per month)']}% per month
            Cost: {b1_data['Cost']}
            
            {battery2}:
            Voltage: {b2_data['Voltage']}
            Lifespan: {b2_data['Lifespan (cycles)']} cycles
            Energy Density: {b2_data['Energy Density (Wh/kg)']} Wh/kg
            Self-Discharge: {b2_data['Self-Discharge (% per month)']}% per month
            Cost: {b2_data['Cost']}
            
            Provide a paragraph comparing their key strengths and weaknesses, and provide use case recommendations.
            """
            
            comparison_response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a battery expert providing detailed technical comparisons."},
                    {"role": "user", "content": comparison_prompt}
                ],
                max_tokens=300
            )
            
            st.write(comparison_response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Error generating comparison: {e}")

# RECYCLING INFO PAGE
elif app_mode == "Recycling Info":
    st.title("♻️ Battery Recycling Guide")
    
    st.markdown("""
    ## Why Recycle Batteries?
    
    Batteries contain materials that can be harmful to the environment if not disposed of properly. 
    Recycling batteries helps recover valuable materials and prevents toxic substances from contaminating soil and water.
    """)
    
    # Recycling information by battery type
    st.subheader("Recycling Instructions by Battery Type")
    
    battery_type = st.selectbox(
        "Select battery type for recycling information:",
        ["Alkaline", "Lithium-ion", "NiMH", "NiCd", "Lead Acid", "Button Cell"]
    )
    
    # Display recycling information based on selection
    if battery_type:
        try:
            recycling_response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a battery recycling expert. Provide detailed recycling instructions."},
                    {"role": "user", "content": f"Provide detailed recycling instructions for {battery_type} batteries. Include safety precautions, preparation steps, and where to recycle them."}
                ],
                max_tokens=400
            )
            
            st.markdown(recycling_response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Error generating recycling information: {e}")
    
    # Recycling locator
    st.subheader("📍 Battery Recycling Locator")
    
    zip_code = st.text_input("Enter your ZIP code to find nearby recycling locations:")
    
    if zip_code and st.button("Find Recycling Locations"):
        st.info("This feature would connect to a recycling location API. For demonstration purposes, here are sample locations.")
        
        st.markdown("""
        ### Nearby Recycling Locations:
        
        1. **City Recycling Center**
           - 123 Green St, Your City
           - 2.3 miles away
           - Accepts all battery types
        
        2. **Hardware Store**
           - 456 Main St, Your City
           - 3.1 miles away
           - Accepts household batteries only
           
        3. **Electronics Retailer**
           - 789 Tech Blvd, Your City
           - 4.5 miles away
           - Accepts rechargeable batteries
        """)

# USAGE HISTORY PAGE
elif app_mode == "Usage History":
    st.title("📝 Battery Analysis History")
    
    if len(st.session_state.battery_history) == 0:
        st.info("You haven't analyzed any batteries yet. Try uploading a battery image in the Battery Analyzer tab.")
    else:
        st.write(f"You have analyzed {len(st.session_state.battery_history)} batteries.")
        
        # Stats and visualizations
        if st.session_state.battery_type_counts:
            st.subheader("Battery Types Statistics")
            
            # Create pie chart of battery types
            fig, ax = plt.subplots(figsize=(8, 6))
            labels = list(st.session_state.battery_type_counts.keys())
            sizes = list(st.session_state.battery_type_counts.values())
            
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
            ax.axis('equal')
            st.pyplot(fig)
        
        # Display battery history entries
        st.subheader("Battery Analysis Entries")
        
        for i, entry in enumerate(reversed(st.session_state.battery_history)):
            with st.expander(f"{entry['timestamp']} - {entry['type']} Battery"):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    # Display the image
                    st.image(f"data:image/png;base64,{entry['image']}", width=150)
                
                with col2:
                    st.markdown(entry['details'])
                
                if st.button("Remove Entry", key=f"remove_{i}"):
                    # Remove entry from history
                    st.session_state.battery_history.remove(entry)
                    
                    # Update type counts
                    if entry['type'] in st.session_state.battery_type_counts:
                        st.session_state.battery_type_counts[entry['type']] -= 1
                        if st.session_state.battery_type_counts[entry['type']] == 0:
                            del st.session_state.battery_type_counts[entry['type']]
                    
                    st.success("Entry removed!")
                    st.experimental_rerun()
        
        # Clear history button
        if st.button("Clear All History"):
            st.session_state.battery_history = []
            st.session_state.battery_type_counts = {}
            st.success("History cleared!")
            st.experimental_rerun()

# Add footer
st.markdown("""
---
📋 **Battery Hub** - One Spot for Batteries  
Developed by Keerthana J and Thoufeeq Mohammed M
""", unsafe_allow_html=True)
