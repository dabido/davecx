/*jslint browser: true*/
/*global $, prettyDate*/

$(document).ready(function () {
	"use strict";
	var load_blogposts, init, parse_tweet;

	load_blogposts = function (feed_uri, element, callback) {
		$.get(feed_uri, function (data) {
			callback(element, data);
		}, "json");
	};

	parse_tweet = function (str) {
		var create_link = function (url, text) {
			var link = $("<a>", {
				text: text,
				href: url,
				target: "_blank"
			});

			return link.prop('outerHTML');
		};

		// parse URLs
		str = str.replace(/[A-Za-z]+:\/\/[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&~\?\/.=]+/g, function (s) {
			return create_link(s, s);
		});

		// parse username
		str = str.replace(/[@]+[A-Za-z0-9_]+/g, function (s) {
			return create_link("http://twitter.com/" + s.replace('@', ''), s);
		});

		// parse hashtags
		str = str.replace(/[#]+[A-Za-z0-9_]+/g, function (s) {
			return create_link("http://search.twitter.com/search?q=" + s.replace('#', ''), s);
		});

		return str;
	};

	init = (function () {
		/* Load blogposts */
		var urls, elements, j, i, url, element, ul;
		urls = [
			"/feed/blog.json",
			"/feed/thoughts.json"
		];

		elements = [
			$(".posts_blog ul"),
			$(".posts_thoughts ul")
		];

		for (j = 0; j < urls.length; j += 1) {
			url = urls[j];
			element = elements[j];

			if (element.length !== 0) {
				// Pass element. Racing condition because of async loading
				load_blogposts(url, element, function (element, data) {
					element.html("");
					for (i = 0; i < data.length; i += 1) {
						element.append("<li><a target='_blank' href='" + data[i].url + "'>" + data[i].title + "</a></li>");

						if (i === 4) {
							break;
						}
					}
				});
			}
		}

		/* Load twitter */
		if ($(".twitterfeed").length !== 0) {
			ul = $(".twitterfeed ul");
			$.get("https://api.twitter.com/1/statuses/user_timeline/davicorn.json?count=10&callback=?", function (data) {
				ul.html("");
				for (i = 0; i < data.length; i += 1) {
					ul.append("<li class='tweet'>" + parse_tweet(data[i].text) + "<p><a target='_blank' href='https://twitter.com/davicorn/status/" + data[i].id_str + "' title=''>" + prettyDate(data[i].created_at) + "</a></p></li>");
				}
				$(".tweet p").css("display", "none");
				$(".tweet").hover(function () {
					$(this).find("p").slideToggle("fast");
				});
			}, "json");
		}
	}());
});