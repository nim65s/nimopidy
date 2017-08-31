import React from 'react';
import { Col, ControlLabel, Checkbox, FormGroup, Form, Glyphicon, Table, Button, FormControl } from 'react-bootstrap';
import './search.css';

class Result extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      added: false,
    }
  }

  add() {
    this.props.mopidy.tracklist.add({uri: this.props.result.uri});
    this.setState({ added: this.props.result.uri });
  }

  render () {
    var length = new Date(this.props.result.length).toISOString().substr(14,5);
    return (
      <tr>
        <td>
          <Button bsSize="sm" bsStyle={this.state.added === this.props.result.uri ? "success" : ""}
            onClick={this.add.bind(this)} disabled={this.state.added === this.props.result.uri }>
            <Glyphicon glyph={this.state.added === this.props.result.uri ? "ok" : "plus"} />
          </Button>
        </td>
        <td>{this.props.result.name}</td>
        <td>{this.props.result.artists ? this.props.result.artists[0].name : ''}</td>
        <td>{this.props.result.album ? this.props.result.album.name : ''}</td>
        <td>{this.props.uri.split(':')[0]}</td>
        <td>{length}</td>
      </tr>
    );
  }
}

class Search extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      any: '',
      results: [],
      searching: false,
      uris: ["spotify:"],
    }
  }

  handleAny(event) { this.setState({ any: event.target.value}); }
  handleUris(event) {
    var uris = [];
    for (var i=0; i < event.target.options.length; i++) {
      if (event.target.options[i].selected) { uris.push(event.target.options[i].value); }
    }
    this.setState({uris: uris});
  }

  handleSubmit(event) {
    if (this.state.any) {
      this.setState({searching: true});
      this.props.mopidy.library.search({any: this.state.any.split(' '), uris: this.state.uris})
        .done(results => this.setState({results: results, searching: false}));
    }
    event.preventDefault();
  }

  render() {
    var results = [];
    if (this.state.results) {
      for (var i = 0; i < this.state.results.length; i++) {
        if (this.state.results[i].tracks) {
          for (var j = 0; j < this.state.results[i].tracks.length; j++) {
            results.push(<Result result={this.state.results[i].tracks[j]} uri={this.state.results[i].uri} mopidy={this.props.mopidy} />);
          }
        }
      }
    }
    return (
      <div>
        <Form horizontal onSubmit={this.handleSubmit.bind(this)}>
          <FormGroup>
            <Col componentClass={ControlLabel} sm={2}>Query</Col>
            <Col sm={10} ><FormControl type="text" placeholder="Query" value={this.state.value} onChange={this.handleAny.bind(this)} /></Col>
          </FormGroup>
          <FormGroup controlId="uris">
            <Col componentClass={ControlLabel} sm={2}>Sources</Col>
            <Col sm={10}><FormControl componentClass="select" multiple value={this.state.uris} onChange={this.handleUris.bind(this)} >
              <option value="spotify:">Spotify</option>
              <option value="youtube:">Youtube</option>
              <option value="local:">Local</option>
            </FormControl></Col>
          </FormGroup>
          <FormGroup>
            <Col smOffset={2} sm={10}>
              <Button bsSize="lg" type="submit"><Glyphicon glyph={this.state.searching ? "refresh" : "search"} /></Button>
            </Col>
          </FormGroup>
        </Form>
        <Table striped condensed hover>
          <thead>
            <tr>
              <th></th>
              <th>Title</th>
              <th>Artist</th>
              <th>Album</th>
              <th>Source</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {results}
          </tbody>
        </Table>
      </div>
      );
  }
}

export default Search;
