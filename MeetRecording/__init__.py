# First, initialize the recordingData object
init_script = """
window.recordingData = {
    mediaRecorder: null,
    stream: null,
    active: false
};
"""
recording_script = """
async function startRecording(filename) {
    try {
        const stream = await navigator.mediaDevices.getDisplayMedia({ 
            video: {
                displaySurface: 'monitor',
                logicalSurface: true,
                cursor: 'always'
            },
            audio: {
                autoGainControl: false,
                echoCancellation: false,
                noiseSuppression: false,
                channelCount: 2,
                sampleRate: 44100
            },
            preferCurrentTab: true,
            systemAudio: 'include'
        });

        const options = {
            mimeType: 'video/webm;codecs=vp8,opus',
            videoBitsPerSecond: 2500000,
            audioBitsPerSecond: 128000
        };

        const mediaRecorder = new MediaRecorder(stream, options);
        let recordedChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        window.recordingData.filename = filename;

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = window.recordingData.filename || 'recording.webm';
            document.body.appendChild(a);
            a.click();
            setTimeout(() => {
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }, 100);
        };

        window.recordingData.mediaRecorder = mediaRecorder;
        window.recordingData.stream = stream;
        window.recordingData.active = true;

        mediaRecorder.start(1000);
        return true;
    } catch (err) {
        console.error('Error:', err);
        return false;
    }
}
return startRecording(arguments[0]);
"""
stop_script = """
if (window.recordingData && window.recordingData.active) {
    if (window.recordingData.stream) {
        window.recordingData.stream.getTracks().forEach(track => track.stop());
    }
    if (window.recordingData.mediaRecorder) {
        window.recordingData.mediaRecorder.stop();
    }
    window.recordingData.active = false;
    return true;
}
return false;
"""