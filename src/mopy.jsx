import React from 'react';
import { Button, ButtonGroup, Glyphicon } from 'react-bootstrap';
import intersperse from './intersperse';
import Mopidy from 'mopidy';
import Progress from './progress';
import ReactMarkdown from 'react-markdown';

class CurrentTrack extends React.Component {
  render() {
    if (this.props.track) {
      if (this.props.track.artists) {
        var artists = this.props.track.artists.map((artist) => <span key={artist.name}>{artist.name}</span>);
        artists = intersperse(artists, ", ");
      } else {
        var artists = '?';
      }
      var album = this.props.track.album ? this.props.track.album.name : '?';
      return (
        <div>
          <img src={this.props.albumCover} alt={album} className="pull-left" />
          <h1>{artists}</h1>
          <h2>{album}</h2>
          <h3>{this.props.track.name}</h3>
        </div>
        );
    }
    return (<div />);
  }
}

class Controls extends React.Component {
  constructor(props) {
    super(props);
    this.handlers = this.handlers.bind(this);
  }

  handlers(e) { this.props.handlers(e.target.name || e.target.parentElement.name); }

  render() {
    return (
      <ButtonGroup>
        <Button bsSize="large" onClick={this.handlers} disabled={!this.props.status} name="previous"><Glyphicon glyph="step-backward" /></Button>
        <Button bsSize="large" onClick={this.handlers} disabled={!this.props.status} name="play"    ><Glyphicon glyph="play"          /></Button>
        <Button bsSize="large" onClick={this.handlers} disabled={!this.props.status} name="pause"   ><Glyphicon glyph="pause"         /></Button>
        <Button bsSize="large" onClick={this.handlers} disabled={!this.props.status} name="stop"    ><Glyphicon glyph="stop"          /></Button>
        <Button bsSize="large" onClick={this.handlers} disabled={!this.props.status} name="next"    ><Glyphicon glyph="step-forward"  /></Button>
      </ButtonGroup>
    );
  }
}

class Lyrics extends React.Component {
  render() {
    return (
      <ReactMarkdown source={this.props.lyrics} />
    );
  }
}

class Mopy extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      connected: false,
      track: false,
      length: 100,
      now: 0,
      volume: 100,
      mute: false,
      muteIcon: "volume-up",
      lyrics: '',
      albumCover: '',
    }
    this.updateTimePosition = this.updateTimePosition.bind(this)
    this.updateCurrentTrack = this.updateCurrentTrack.bind(this)
    this.updateVolume = this.updateVolume.bind(this)
    this.updateMute = this.updateMute.bind(this)
    this.controlHandlers = this.controlHandlers.bind(this)
    this.onSeek = this.onSeek.bind(this)
    this.onVolume = this.onVolume.bind(this)
    this.onMute = this.onMute.bind(this)
  }

  componentDidMount() {
    this.mopidy = new Mopidy({
      webSocketUrl: 'ws://' + this.props.url + ':6680/mopidy/ws/',
      callingConvention: 'by-position-or-by-name'
    });
    this.mopidy.on("state:online", () => {this.setState({connected:true}); this.requestAll();});
    this.mopidy.on("state:offline", () => {this.setState({connected:false});});
    this.mopidy.on('event:trackPlaybackStarted', (e) => { this.updateCurrentTrack(e.tl_track.track); });
    this.mopidy.on('event:volumeChanged', (e) => { this.updateVolume(e.volume); });
    this.mopidy.on('event:muteChanged', (e) => { this.updateMute(e.mute); });
    this.timerIDtp = setInterval(() => {if (this.state.connected) {this.requestTimePosition();}}, 100);
  }

  requestAll() { this.requestCurrentTrack(); this.requestTimePosition(); this.requestVolume(); }
  requestTimePosition() { this.mopidy.playback.getTimePosition().done(this.updateTimePosition); }
  requestCurrentTrack() { this.mopidy.playback.getCurrentTrack().done(this.updateCurrentTrack); }
  requestVolume() {
    this.mopidy.mixer.getVolume().done(this.updateVolume);
    this.mopidy.mixer.getMute().done(this.updateMute);
  }

  updateTimePosition(time) { this.setState({now: time, nowstr: new Date(time).toISOString().substr(14,5)}); }
  updateVolume(vol) { this.setState({volume: vol}); }
  updateMute(mute) { this.setState({mute: mute, muteIcon: mute ? "volume-off" : "volume-up"}); }
  updateCurrentTrack(track) {
    if (track) {
      fetch('http://' + this.props.url + ':8000/songs/?uri=' + track.uri).then(result => result.json())
        .then(items => { if (items.count === 1) {
          this.setState({lyrics: items.results[0].lyrics});
        } else {
          var payload = JSON.stringify({ uri: track.uri, artist: (track.artists ? track.artists[0].name : '?'),
            title: track.name });
          fetch('http://' + this.props.url + ':8000/songs/', {
            method: 'POST', headers: {'Content-Type': 'application/json'}, body: payload
          }).catch(error => this.updateCurrentTrack(track))
            .then(results => results.json()).then(resp => this.setState({lyrics: resp.lyrics}))
            .catch(error => this.updateCurrentTrack(track));
        }});
      if (track.album) {
        fetch('https://api.spotify.com/v1/albums/' + track.album.uri.substring(14)).then(result => result.json())
          .then(data => this.setState({albumCover: data.images[1].url}));
      }
      this.setState({track: track, length: track.length, lyrics: ''});
    }
  }

  onSeek(time) { this.setState({now: time}); this.mopidy.playback.seek({'time_position': time}); }
  onVolume(vol) { this.mopidy.mixer.setVolume({'volume': vol}); }
  onMute() { this.mopidy.mixer.setMute({"mute": !this.state.mute}); }

  componentWillUnmount() {
    this.mopidy.close();
    this.mopidy.off();
    this.mopidy = null;
    clearInterval(this.timerIDtp);
  }

  controlHandlers(command) { if (this.state.connected) { this.mopidy.playback[command](); }}

  render() {
    return (
      <div>
        <CurrentTrack track={this.state.track} albumCover={this.state.albumCover} />
        <Controls handlers={this.controlHandlers} status={this.state.connected} />
        <Button bsSize="large" onClick={this.onMute} disabled={!this.state.connected}>
          <Glyphicon glyph={this.state.muteIcon} /></Button>
        <Progress onSeek={this.onVolume} max={100} now={this.state.volume} label={this.state.volume} wheelCoef={.1} />
        <Progress onSeek={this.onSeek} max={this.state.length} now={this.state.now} label={this.state.nowstr}
          wheelCoef={100} active />
        <div className="clearfix" />
        <Lyrics lyrics={this.state.lyrics} />
      </div>
      );
  }
}

export default Mopy;
