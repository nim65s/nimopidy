import React from 'react';
import { ProgressBar } from 'react-bootstrap';

class Progress extends React.Component {
  constructor(props) {
    super(props);
    this.click = this.click.bind(this);
  }

  click(event) {
    var element = (event.target.parentElement.classList[0] === "progress" ? event.target.parentElement : event.target);
    var rectangle = element.getBoundingClientRect();
    this.props.onSeek(Math.round((event.pageX - rectangle.left) * this.props.max / rectangle.width));
  }

  render() {
    return (
      <ProgressBar active max={this.props.max} now={this.props.now} onClick={this.click} />
    );
  }
}

export default Progress;
