import React, { useRef, useEffect } from 'react';

function Camera() {
  const videoRef = useRef(null);

  useEffect(() => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch(err => console.error(err));
    }
  }, []);

  return (
    <div className="camera-edit">

      <video ref={videoRef} autoPlay />
    </div>
  );
}

export default Camera;
