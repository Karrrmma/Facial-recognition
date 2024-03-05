import { useNavigate } from 'react-router-dom';

function Button(){
    const navigate = useNavigate();
    const handleClick = () =>{
        navigate('/camera');
    };

    return(
    <button  onClick={handleClick} className="button"> Click me to start the facial recognition</button>)

}
export default Button