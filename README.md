# Battery-Hub-One-Spot-for-Batteries

# Battery Hub 🔋

## One Spot for All Your Battery Needs

Battery Hub is a comprehensive Streamlit application designed to analyze, identify, and provide detailed information about household batteries through image recognition.

![Image](https://github.com/user-attachments/assets/ee545392-13d4-4e09-b179-5ae528e2acc8)
![Image](https://github.com/user-attachments/assets/d8905d1f-9235-4f51-afce-4c15127811e1)
![Image](https://github.com/user-attachments/assets/1ca99766-b86e-4b8d-8541-b8ede431b65a)
![Image](https://github.com/user-attachments/assets/f41379a0-6b4f-4fc6-ad75-67103b09222c)
![Image](https://github.com/user-attachments/assets/b57653ba-7fc4-4adc-b02e-92ba666b77e7)
![Image](https://github.com/user-attachments/assets/527cca74-34a6-498f-8b65-65cf0b4d56ad)
![Image](https://github.com/user-attachments/assets/42f46213-1dc3-4476-b6ab-bf45f4ad7015)

## Features

### 🔍 Battery Analyzer
Upload images of batteries to:
- Automatically detect if the uploaded image contains a battery
- Identify the battery type, specifications, and details
- Receive safety and handling instructions
- Get compatible alternatives for your battery

### 💬 Interactive Battery Assistant
- Ask questions about the identified battery
- Get real-time responses from our AI-powered battery expert
- Learn about battery usage, specifications, and best practices

### 📊 Battery Comparison
- Compare different types of batteries side by side
- Visualize key metrics like voltage, lifespan, energy density
- Get detailed analysis of strengths and weaknesses
- Receive use case recommendations

### ♻️ Recycling Information
- Access detailed recycling instructions for different battery types
- Learn about proper disposal methods
- Find nearby recycling locations (demo feature)

### 📝 Battery Usage History
- Track all your analyzed batteries
- View statistics on your battery usage
- Monitor types of batteries you use most frequently

## Technical Details

### Technologies Used
- **Frontend**: Streamlit for UI/UX
- **AI Services**: OpenAI GPT-4 Vision API for image analysis and chatbot
- **Image Processing**: PIL for image handling
- **Data Visualization**: Matplotlib for charts and graphs
- **Machine Learning**: TensorFlow for battery detection model

### Battery Detection Model
The application uses a pre-trained TensorFlow model to validate whether an uploaded image contains a battery before proceeding with detailed analysis.

## Installation & Setup

### Requirements
- Python 3.7+
- Streamlit
- OpenAI API key
- TensorFlow 2.x
- Other dependencies listed in requirements.txt

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/itzz-keerthi/Battery-Hub-One-Spot-for-Batteries.git
cd battery-hub
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Navigate to the Battery Analyzer section
2. Upload a clear image of a battery
3. The system will first verify if the image contains a battery
4. If verified, click "Analyze Battery" to get detailed information
5. Use the chat feature to ask questions about the identified battery
6. Explore other sections for battery comparisons and recycling information

## Future Enhancements

- Real-time battery detection through camera feed
- Integration with e-commerce APIs for battery replacement ordering
- Battery health prediction based on usage patterns
- Mobile app version for on-the-go battery identification
- Expanded database of battery types and specifications
