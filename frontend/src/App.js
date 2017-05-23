import React, { Component } from 'react';
import TrackSearcher from './Tracks';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>Spotify Playlist Curator</h2>
        </div>
        <TrackSearcher />
      </div>
    );
  }
}

export default App;
