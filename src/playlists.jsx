import React from 'react';
import { ButtonGroup, Glyphicon, Table, Button } from 'react-bootstrap';

class PlayList extends React.Component {
  render() {
    return (
      <tr>
        <td><Button><Glyphicon glyph="check" /></Button></td>
        <td>{this.props.name}</td>
        <td>{this.props.uri}</td>
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
    setTimeout(this.updatePlaylists, 1000);
  }

  updatePlaylists() {
    this.props.mopidy.playlists.getPlaylists({include_tracks: false}).done(playlists => this.setState({playlists: playlists}));
  }

  render() {
    if (this.state.playlists) {
      var playlists = [];
      for (var i = 0; i < this.state.playlists.length; i++) {
        playlists.push(<PlayList name={this.state.playlists[i].name} uri={this.state.playlists[i].uri} mopidy={this.props.mopidy} />);
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
