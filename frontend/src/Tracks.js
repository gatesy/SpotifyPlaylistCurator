import React, { Component } from 'react';

class Track extends Component {
    render() {
        return (
            <li>{this.props.track.name}</li>
        );
    }
}

class TrackList extends Component {
    render() {
        const trackListItems = this.props.tracks.map((track) => (
          <Track key={track.id} track={track}/>
        ));
        return (
            <ul>
                {trackListItems}
            </ul>
        );
    }
}

class SearchForTracks extends Component {
    constructor(props) {
        super(props);
        this.state = {'searchTerm' : "Danger Zone"};
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Track name:
                    <input type="text" value={this.state.searchTerm} onChange={this.handleChange}/>
                </label>
                <input type="submit" value="Search"/>
            </form>
        );
    }

    handleChange(event) {
        this.setState({'searchTerm' : event.target.value});
    }

    handleSubmit(event) {
        let self = this;
        let params = {'term': this.state.searchTerm };
        let url = "http://localhost:8888/search?" + encodeQueryData(params);

        fetch(url).then(function(response) {
        if(response.ok) {
            return response.json();
        }
        throw new Error('Response not ok')
        }).then(function(data) {
            let tracks = data.tracks.items;
            console.log(data);
            self.props.onTracks(tracks);
        }).catch(function(err) {  
            console.log('Fetch Error: ', err);  
        });
        event.preventDefault();
  };
}

class TrackSearcher extends Component {
  constructor(props) {
    super(props);
    this.state = {'tracks' : []};
    this.handleTracks = this.handleTracks.bind(this);
  }

  render() {
    return (
      <div>
        <SearchForTracks onTracks={this.handleTracks} />
        <TrackList tracks={this.state.tracks} />
      </div>
    );
  }

  handleTracks(tracks) {
    this.setState({'tracks' : tracks});
  }
}

function encodeQueryData(data) {
   let ret = [];
   for (let d in data)
     ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
   return ret.join('&');
}

export default TrackSearcher;