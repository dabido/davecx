var app = angular.module('davecx', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

var getOffset = function(elem) {
 	var docElem, win, box = {
        top: 0,
        left: 0
    };

	var docElem = document.documentElement;
	var win = window;
	var box = elem.getBoundingClientRect();

    return {
        top: box.top + (win.pageYOffset || docElem.scrollTop) - (docElem.clientTop || 0),
        left: box.left + (win.pageXOffset || docElem.scrollLeft) - (docElem.clientLeft || 0)
    };
};

app.directive('hideMenuOnClick', function ($window) {
	return function($scope, element, attrs) {
		angular.element($window).on('click', function (ev) {
			if (ev.target !== undefined && ev.target.attributes !== undefined) {
				var attributes = ev.target.attributes;
				for (index in attributes) {
					if (attributes[index].name !== undefined && attributes[index].name.indexOf('ng-click') != -1) {
						return;
					}
				}
			}

			if ($scope.show_categories !== false) {
				$scope.$apply(function () {
					$scope.show_categories = false;
					$scope.$digest();
				});
			}
		});
	};
});

app.directive('sharebutton', function ($window) {
	return function(scope, element, attrs) {
		var el = angular.element(element);
		el.on('click', function (event) {
			window.open(el.attr('href'), 'Share on ' + el.attr('sharebutton'), 'width=626,height=436,top=100,left=100');
			event.preventDefault();
			return false;
		});
	};
});

app.directive('followingInfobox', function ($window) {
	return function(scope, element, attrs) {
		var windowEl = angular.element($window);
		var elementOffset = getOffset(element[0]);
		var elementHeight = element[0].clientHeight;
		windowEl.on('scroll', function() {
			var wrapper = angular.element(element).parent()[0].querySelector('.flow');
			var wrapperHeight = wrapper.clientHeight;
			var wrapperOffset = getOffset(wrapper);

			var windowScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
			if (windowScrollPosition > elementOffset.top && windowScrollPosition < (wrapperOffset.top + wrapperHeight - elementHeight)) {
				var difference = windowScrollPosition - wrapperOffset.top;
				angular.element(element).css('top', difference + 'px');
			} else if (windowScrollPosition > (wrapperOffset.top + wrapperHeight - elementHeight)) {
				if (wrapperHeight - elementHeight > 0) {
					angular.element(element).css('top', (wrapperHeight - elementHeight) + 'px');
				}
			} else if (windowScrollPosition < wrapperOffset.top) {
				angular.element(element).css('top', '0px');
			}
		});
	};
});

app.controller('MainController', function($scope, $window) {
	$scope.scroll = 0;
	$scope.show_categories = false;

	$scope.test = function (selector) {
		var element = document.querySelector(selector);
		return getOffset(element).top;
	};
});