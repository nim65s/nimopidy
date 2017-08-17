import React from 'react';
import { Button, ButtonGroup, Glyphicon } from 'react-bootstrap';
import Mopidy from 'mopidy';
import Progress from './progress';
import Volume from './volume';
import Snap from './snap';
import ReactMarkdown from 'react-markdown';
import WebSocket from 'react-websocket';

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

class Mopy extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      connected: false,
      now: 0,
      nowstr: '',
      volume: 100,
      mute: false,
      track: '',
      state: '',
      snapclients: '',
    }
    this.controlHandlers = this.controlHandlers.bind(this)
    this.updateVolume = this.updateVolume.bind(this)
    this.updateMute = this.updateMute.bind(this)
    this.onMute = this.onMute.bind(this)
  }

  componentDidMount() {
    this.mopidy = new Mopidy({
      webSocketUrl: 'ws://' + window.location.hostname + ':6680/mopidy/ws/',
      callingConvention: 'by-position-or-by-name'
    });
    this.mopidy.on("state:online", () => {this.setState({connected:true}); });
    this.mopidy.on("state:offline", () => {this.setState({connected:false});});
    this.mopidy.on('event:volumeChanged', (e) => { this.updateVolume(e.volume); });
    this.mopidy.on('event:muteChanged', (e) => { this.updateMute(e.mute); });
  }

  updateVolume(vol) { this.setState({volume: vol}); }
  updateMute(mute) { this.setState({mute: mute, muteIcon: mute ? "volume-off" : "volume-up"}); }

  handleData(data) {
    let result = JSON.parse(data);
    if (result.track) this.setState({track: result.track});
    if (result.state) this.setState({state: result.state});
    if (result.snapclients) this.setState({snapclients: result.snapclients});
    if (result.time_position) {
      this.setState({now: result.time_position, nowstr: new Date(result.time_position).toISOString().substr(14,5)});
    }
  }

  onSeek(time) {
    var t = Math.min(this.state.track.length, Math.max(0, time));
    this.setState({now: t});
    this.mopidy.playback.seek({'time_position': t});
  }
  onVolume(vol) { this.mopidy.mixer.setVolume({'volume': Math.min(100, Math.max(0, vol))}); }
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
        <div className="clearfix">
          <img src={this.state.track.cover} alt={this.state.track.album} className="pull-left" />
          <h1>{this.state.track.artists}</h1>
          <h2>{this.state.track.name}</h2>
          <h3>{this.state.track.album}</h3>
          <Controls handlers={this.controlHandlers} status={this.state.connected} />
          <Progress onSeek={this.onSeek.bind(this)} max={this.state.track.length} now={this.state.now} label={this.state.nowstr} wheelCoef={100} active />
        </div>
        <h2>Volume</h2>
        <Volume onVolume={this.onVolume.bind(this)} now={this.state.volume} name="général" onMute={this.onMute.bind(this)} muted={this.state.mute} />
        <Snap snapclients={this.state.snapclients} />
        <h2>Lyrics</h2>
        <ButtonGroup>
          <Button href={'http://' + window.location.hostname + '/change/' + this.state.track.uri}>Change</Button>
          <Button href={'http://' + window.location.hostname + '/update/' + this.state.track.uri}>Update</Button>
        </ButtonGroup>
        <ReactMarkdown source={this.state.track.lyrics} />
        <WebSocket url={'ws://' + window.location.hostname} onMessage={this.handleData.bind(this)} />
      </div>
    );
  }
}

export default Mopy;
