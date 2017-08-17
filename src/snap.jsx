import React from 'react';
import Volume from './volume';

class SnapClient extends React.Component {
  post(muted, percent) {
    fetch("/snapcast", { method: "POST", body: JSON.stringify({
      'id': this.props.client.mac,
      'volume': {'muted': muted, 'percent': percent}
    })});
  }

  onMute() { this.post(!this.props.client.muted, this.props.client.percent); }
  onVolume(vol) { this.post(this.props.client.muted, Math.min(100, Math.max(0, vol))) }

  render() {
    return (
      <Volume onVolume={this.onVolume.bind(this)} now={this.props.client.percent} name={this.props.client.name}
      onMute={this.onMute.bind(this)} muted={this.props.client.muted} />
    );
  }
}

class Snap extends React.Component {
  render() {
    var clients = [];
    for (var i = 0; i < this.props.snapclients.length; i++) {
      clients.push(<SnapClient client={this.props.snapclients[i]} />);
    }
    return (
      <div>{clients}</div>
      );
  }
}

export default Snap;
