/*jslint browser: true*/
/*global $, prettyDate*/

$(document).ready(function () {
	"use strict";
	$('.tooltip').qtip({
		content: {
			attr: 'alt'
		},
		style: {
			classes: 'ui-tooltip-youtube'
		},
		position: {
			my: "bottom center",
			at: "top center"
		}
	});
});