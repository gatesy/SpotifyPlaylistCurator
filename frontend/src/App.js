import React, { Component } from 'react';
import './App.css';

class Tracks extends React.Component {
  constructor(props) {
    super(props);
    this.state = {'tracks': []};
    this.componentDidMount = this.componentDidMount.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  };

  handleChange(event) {
    this.setState({'search_term' : event.target.value});
  }

  handleSubmit(event) {
    this.search(this.state.search_term);
    event.preventDefault();
  }

  render() {
    const listItems = this.state.tracks.map((item) => 
      <li key={item.id}>
        {item.name}
      </li>
    );

    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <label>
            Track name:
            <input type="text" value={this.state.searchTerm} onChange={this.handleChange}/>
          </label>
          <input type="submit" value="Search"/>
        </form>
        <ul>
          {listItems}
        </ul>
      </div>
    );
  };

  search(term) {
    var self = this;
    let params = {'term': term };
    let url = "http://localhost:8888/search?" + encodeQueryData(params);

    fetch(url).then(function(response) {
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

  componentDidMount() {
    this.search("Danger Zone");
  };
}

function encodeQueryData(data) {
   let ret = [];
   for (let d in data)
     ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
   return ret.join('&');
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
