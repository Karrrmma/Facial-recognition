import Header from './Header.jsx'
import Button from './Button.jsx'
import Camera from './Camera';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  
  return (
    <Router>  
        <Header/>
        <Routes>
        <Route path="/" element={<Button />} />
        <Route className = "camera-edit" path="/camera" element={<Camera />} />
        </Routes>
          
    </Router>
    
  );
}
export default App
