import React, { Component } from 'react';
import './App.css';

class Tracks extends React.Component {
  constructor(props) {
    super(props);
    this.state = {'tracks': []};
    this.componentDidMount = this.componentDidMount.bind(this);
  };

  render() {
    const listItems = this.state.tracks.map((item) => 
      <li key={item.id}>
        {item.name}
      </li>
    );

    return (
      <div>
        <ul>
          {listItems}
        </ul>
      </div>
    );
  };

  componentDidMount() {
    var self = this;
    fetch("http://localhost:8888/search?term=Danger%20Zone").then(function(response) {
      if(response.ok) {
        return response.json();
      }
      throw new Error('Response not ok')
    }).then(function(data) {
      let tracks = data.tracks.items;
      console.log(data);
      self.setState({'tracks': tracks});
    }).catch(function(err) {  
      console.log('Fetch Error: ', err);  
    });
  };
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <h2>Spotify Playlist Curator</h2>
        </div>
        <Tracks/>
      </div>
    );
  }
}

export default App;
