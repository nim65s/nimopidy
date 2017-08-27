import React from 'react';
import { Table } from 'react-bootstrap';

class Track extends React.Component {
  render() {
    var length = new Date(this.props.track.track.length).toISOString().substr(14,5);
    return (
      <tr>
        <td>{this.props.track.tlid}</td>
        <td>{this.props.track.track.name}</td>
        <td>{this.props.track.track.artists[0].name}</td>
        <td>{this.props.track.track.album.name}</td>
        <td>{length}</td>
      </tr>
    );
  }
}

class TrackList extends React.Component {
  render() {
    var tracks = [];
    if (this.props.tracks) {
      for (var i = this.props.max * (this.props.page - 1); i < Math.min(this.props.tracks.length, this.props.max * this.props.page); i++) {
        tracks.push(<Track track={this.props.tracks[i]} />);
      }
    }
    return (
      <Table striped condensed hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Title</th>
            <th>Artist</th>
            <th>Album</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {tracks}
        </tbody>
      </Table>
      );
  }
}

export default TrackList;
