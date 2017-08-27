import React from 'react';
import { Glyphicon, Table, Button } from 'react-bootstrap';

class PlayList extends React.Component {
  activate() {
    fetch('/playlists', {method: 'POST', body: JSON.stringify({
      'uri': this.props.playlist.uri, 'active': !this.props.playlist.active})})
      .then(this.props.updatePlaylists);
  }

  render() {
    return (
      <tr>
        <td><Button onClick={this.activate.bind(this)}><Glyphicon glyph={this.props.playlist.active ? "check" : "unchecked"} /></Button></td>
        <td>{this.props.playlist.name}</td>
        <td>{this.props.playlist.uri}</td>
      </tr>
    );
  }
}

class PlayLists extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      playlists: [],
    }
    this.updatePlaylists = this.updatePlaylists.bind(this)
    this.updatePlaylists();
    setInterval(this.updatePlaylists, 300000);
  }

  updatePlaylists() {
    fetch('/playlists').then(r => r.json()).then(data => this.setState({playlists: data.playlists}));
  }

  render() {
    if (this.state.playlists) {
      var playlists = [];
      for (var i = 0; i < this.state.playlists.length; i++) {
        playlists.push(<PlayList playlist={this.state.playlists[i]} updatePlaylists={this.updatePlaylists} />);
      }
      return (
        <Table striped condensed hover>
          {playlists}
        </Table>
        );
    } else { return <Table />; }
  }
}

export default PlayLists;
