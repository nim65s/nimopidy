import React from 'react';
import { ButtonGroup, Glyphicon, Table, Button } from 'react-bootstrap';
import './tracklist.css';

class Track extends React.Component {

  first() { this.props.mopidy.tracklist.move({ start: this.props.n, end: this.props.n, to_position: 1}); }
  up() { this.props.mopidy.tracklist.move({ start: this.props.n, end: this.props.n, to_position: this.props.n-1}); }
  down() { this.props.mopidy.tracklist.move({ start: this.props.n, end: this.props.n, to_position: this.props.n+1}); }
  del() { this.props.mopidy.tracklist.remove({ tlid: [this.props.track.tlid] }); }

  render() {
    if (this.props.track) {
    var length = new Date(this.props.track.track.length).toISOString().substr(14,5);
    return (
      <tr>
        <td>{this.props.track.track.name}</td>
        <td>{this.props.track.track.artists ? this.props.track.track.artists[0].name : ''}</td>
        <td>{this.props.track.track.album ? this.props.track.track.album.name : ''}</td>
        <td>{length}</td>
        <td><ButtonGroup>
          <Button bsSize="xs" onClick={this.first.bind(this)} disabled={this.props.n < 2} ><Glyphicon glyph="chevron-up" /></Button>
          <Button bsSize="xs" onClick={this.up.bind(this)} disabled={this.props.n < 2} ><Glyphicon glyph="menu-up" /></Button>
          <Button bsSize="xs" onClick={this.down.bind(this)} disabled={this.props.n < 1} ><Glyphicon glyph="menu-down" /></Button>
          <Button bsSize="xs" onClick={this.del.bind(this)} disabled={this.props.n < 1} ><Glyphicon glyph="remove" /></Button>
        </ButtonGroup></td>
      </tr>
    );
    } else { return <tr />; }
  }
}

class TrackList extends React.Component {
  render() {
    if (this.props.tracks) {
    var tracks = [];
      for (var i = 0; i < this.props.tracks.length; i++) {
        tracks.push(<Track track={this.props.tracks[i]} n={i} mopidy={this.props.mopidy} />);
      }
    return (
      <Table striped condensed hover>
        <thead>
          <tr>
            <th>Title</th>
            <th>Artist</th>
            <th>Album</th>
            <th>Time</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {tracks}
        </tbody>
      </Table>
      );
    } else { return <Table />; }
  }
}

export default TrackList;
