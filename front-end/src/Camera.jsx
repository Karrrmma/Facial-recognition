import React from 'react';

function Camera() {
    return (
        <div>
            <h1>Live Video Feed</h1>
            <img src="http://localhost:5000/video_feed" alt="Video Feed" />
        </div>
    );
}

export default Camera;
