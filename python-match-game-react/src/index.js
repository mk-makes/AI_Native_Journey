import './index.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // This line is important for Tailwind to be imported
import App from './App'; // This imports your game's App component
// import reportWebVitals from './reportWebVitals'; // You can comment this out or remove if not using

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App /> {/* This renders your game's App component */}
  </React.StrictMode>
);

// If you kept reportWebVitals, you can uncomment this line
// reportWebVitals();