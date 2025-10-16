# eCourts Legal Services Website

A professional web application for eCourts case management with React.js frontend and Flask backend.

## Features

- **CNR Search**: Search cases by CNR number
- **Case Details Search**: Search by case type, number, and year
- **Cause List**: Download today's cause list
- **Professional UI**: Modern, responsive design with legal aesthetics
- **Real-time Results**: Instant search results with detailed case information

## Project Structure

```
ecourts_scrapper/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html     # HTML template
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Styling
│   │   ├── index.js       # React entry point
│   │   └── index.css      # Global styles
│   └── package.json       # Node.js dependencies
├── ecourts_scraper.py     # Original scraper logic
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start React development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/search/cnr` - Search by CNR number
- `POST /api/search/case` - Search by case details
- `GET /api/causelist` - Get today's cause list

## Usage

1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Use the tabs to switch between different search options:
   - **CNR Search**: Enter CNR number and select date
   - **Case Details**: Enter case type, number, year, and date
   - **Cause List**: Download today's complete cause list

## Technologies Used

- **Frontend**: React.js, Axios, Lucide React Icons
- **Backend**: Flask, Flask-CORS
- **Scraping**: BeautifulSoup4, Requests
- **Styling**: Modern CSS with gradients and glassmorphism effects

## Professional Features

- Responsive design for all devices
- Professional color scheme and typography
- Loading states and error handling
- Clean, intuitive user interface
- Formal legal website aesthetics