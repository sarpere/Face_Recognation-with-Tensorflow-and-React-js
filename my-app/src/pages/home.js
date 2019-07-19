import * as React from 'react';
import Uwebcam from '../components/Uwebcam';
import './home.css';

class Home extends React.Component {
    render() {
        return (
            <div>
                <div className="Container">
                <Uwebcam {...this.props}/>
                </div>
            </div>
        );
    }
}

export default Home;