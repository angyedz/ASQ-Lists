# 🎮 ASQ Lists - Modern Web Template

A modern, responsive web application for managing and displaying game level lists with leaderboards and roulette functionality.

## ✨ Features

- **📋 List View** - Display all levels with detailed information about creators, verifiers, and records
- **🏆 Leaderboard** - Real-time player rankings based on earned points
- **🎲 Roulette Mode** - Random level selection for challenges with progress tracking
- **🌙 Dark/Light Mode** - Smooth theme switching with localStorage persistence
- **📱 Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **⚡ Modern UI** - Clean, contemporary design with smooth animations and gradients
- **♿ Accessible** - Semantic HTML and keyboard navigation support

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ (for local development server)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation & Running

```bash
cd "my site"
python server.py
```

Then open your browser to **http://localhost:8000**

## 📁 Project Structure

```
my site/
├── index.html              # Main application entry point
├── server.py              # Local development server
│
├── css/
│   ├── main.css           # Global styles & theme variables
│   ├── reset.css          # CSS reset & normalization
│   ├── typography.css     # Font and text styles
│   ├── components/
│   │   ├── btn.css        # Button component styles
│   │   ├── nav.css        # Navigation styles
│   │   └── tabs.css       # Tab component styles
│   └── pages/
│       ├── list.css       # List page styles
│       ├── leaderboard.css # Leaderboard page styles
│       └── roulette.css   # Roulette page styles
│
├── js/
│   ├── main.js            # Vue app initialization & router setup
│   ├── routes.js          # Application routes
│   ├── store.js           # Reactive state management
│   ├── util.js            # Utility functions (YouTube embedding, etc.)
│   ├── score.js           # Scoring system logic
│   ├── content.js         # Data fetching & processing
│   ├── components/
│   │   ├── Spinner.js     # Loading spinner component
│   │   ├── Btn.js         # Button component
│   │   └── List/
│   │       └── LevelAuthors.js # Level authors display component
│   └── pages/
│       ├── List.js        # List page component
│       ├── Leaderboard.js # Leaderboard page component
│       └── Roulette.js    # Roulette page component
│
├── data/
│   ├── _list.json         # List of level file names
│   ├── _editors.json      # List staff information
│   ├── SampleLevel1.json  # Example level data
│   ├── SAMPLELEVEL2.json  # Example level data
│   └── Sample_Level_3.json # Example level data
│
└── assets/
    └── *.svg              # Icons and graphics
```

## 🎨 Design System

### Color Palette
- **Primary**: `#4f46e5` (Indigo)
- **Primary Light**: `#818cf8`
- **Primary Dark**: `#3730a3`
- **Background**: `#fafbfc` (Light) / `#0f1419` (Dark)
- **Error**: `#ef4444` (Red)
- **Success**: `#10b981` (Green)

### Typography
- **Font**: Lexend Deca (body), System fonts (UI)
- **Sizes**: Responsive scales from 12px to 51px
- **Weight**: 500 (regular), 600 (semi-bold), 700 (bold)

## 🔧 Configuration

### Adding Levels

Create a new JSON file in `/data/` following this structure:

```json
{
  "id": 12345678,
  "name": "Level Name",
  "author": "Creator Name",
  "creators": [],
  "verifier": "Verifier Name",
  "verification": "https://www.youtube.com/watch?v=...",
  "percentToQualify": 50,
  "password": "Password or 'Free to Copy'",
  "records": [
    {
      "user": "Player Name",
      "link": "https://www.youtube.com/watch?v=...",
      "percent": 100,
      "hz": 360,
      "mobile": false
    }
  ]
}
```

Then add the filename to `/data/_list.json`:

```json
[
  "YourNewLevel",
  "SampleLevel1",
  ...
]
```

### Customizing Staff

Edit `/data/_editors.json`:

```json
[
  {
    "role": "owner",
    "name": "Your Name",
    "link": "https://youtube.com/..."
  },
  ...
]
```

Available roles:
- `owner` - List owner
- `admin` - Administrator
- `helper` - Helper
- `trial` - Trial helper
- `dev` - Developer/Coder

## 🎯 Technologies

- **Frontend Framework**: Vue.js 3.2
- **Router**: Vue Router 4.0
- **Styling**: Modern CSS3 with CSS Variables & Grid Layout
- **Build**: ES Modules (native browser support)
- **Server**: Python SimpleHTTPServer (development)

## 📝 License

Original template by [TheShittyList](https://tsl.pages.dev/)
Modified for ASQ Lists

## 🤝 Contributing

Feel free to fork and customize this template for your own list!

## 💡 Tips

- Use **high-quality YouTube thumbnails** for level videos
- Keep **JSON file names consistent** with list entries
- Test in **both light and dark modes**
- Optimize images in `/assets/` for faster loading
- Keep level data updated regularly

---

Made with ❤️ for the gaming community
