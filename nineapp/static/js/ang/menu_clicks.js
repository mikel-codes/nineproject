var csp = angular.module("customParser", ['ngRoute'])
csp.config(['$interpolateProvider', function($interpolateProvider){
	$interpolateProvider.startSymbol("__")
	$interpolateProvider.endSymbol("__")
}]);

csp.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-csrftoken';
}
]);

var app = angular.module("mainApp", ['customParser']);


app.directive("menuDir", function(){
	return{
		restrict: "EACM",
		require: 'ngModel',
		link: function(scope, element, attrs){
			element.on('click', function(event){
				console.log("You clicked " + event.target.innerText)
				setSelected(event.target.innerText)
			})
			var setSelected = function(value){
				var menu_items = element.find("a")
				menu_items.removeClass("active")
				for (var i = menu_items.length - 1; i >= 0; i--) {
					if (menu_items.eq(i).text() === value) {
						menu_items.eq(i).addClass('active')
				}
			}
		}
	}
}
}).controller("menuCtrl", function($scope, $location,$window){
	$scope.getClass = function(url){
		if($location.url() === url){
			console.log("This is for location", $location)
			return "active"

		}
		else
			return ""

	}
})

app.controller("defaultCtrl", function($scope, $anchorScroll, $location, $exceptionHandler){

	$scope.show = function(id){
			$location.hash(id)


	};

	
});

app.controller("timeCtrl", function($scope, $interval){
	$interval(function(){
		$scope.today = new Date().toLocaleTimeString()
	}, 2000);
})

app.directive('viewDir', function($http, $window, $location){
	return{
		restrict: "EACM",
		link: function(scope, element, attrs){
			$window.onload = () =>{
				//$document.element("script").
				console.log("Hurray")
		     	$http.get($location.absUrl()).then((res) => {
		     		scope.$watch(attrs, () => {
		     			const config =  {
		     				withCredentials:{ 'Authorization':  '5163dc3dfd27556c455f2fc3f6ddffa76fe4f8aa'}
		     			};
		
		     			$http.put("https://"+ $location.$$host + attrs.link, config).then((resp) =>{
		     				scope.views = resp.data
		     			},
		     			(err) => {
		     				console.log("js viewer post request errors ", err.data)

		     			})
		     		})
		     		
			},
			(err) => {
				console.log("js viewer for get found these errors ", err)
			});
		}
	}

	}
})
app.directive('vieDir', function($http, $browser, $window, $location){
	return{
		restrict: "EACM",
		link: function(scope, element, attrs){
		    $window.onload = () => {

			$http.get("https://ipinfo.io/json").then(function success(res){
				const ip = res.data.ip
				const country = res.data.country

			},
			function err(data){

			});
		}
	}
	}
})

app.run(['$rootScope', '$location','$document', function($rootScope, $location, $document) {
	$rootScope.$on('$locationChangeSuccess', function(evt, next, previous) {
		var links = $document.find("a")
		links.removeClass('active')
		for (var i = links.length - 1; i >= 0; i--) {
			
			if (links[i].href === next) {
				
				links.eq(i).addClass("active")
			}
		}
	})
}])





app.directive("clapDir", function($http, $document){
	return{
		restrict: "EACM",
		link: function(scope, element, attrs){
			scope.$watch(attrs, function(){
				var tk = (attrs.usertoken).replace(/['']/gi,"")
				 
				var id = attrs.clapid
				var clapper = (attrs.clapper).replace(/[\s\s]/gi,"")
				var owner = (attrs.owner).replace(/[\s\s]/gi, "")
			
				scope.claps = attrs.counter

				element.on('click', function(event){
	
					var config = {
						withCredentials:{ 'Authorization':  tk },
						'num_claps': 1,
						'clapper': clapper,
						'owner': owner

						}

				
					
					$http.put("https://" + $location.$$host + "/clap/" + id + "/by/" + clapper + "/for/" + owner, config).then(
						function success(data, status, config){
							scope.claps = data.data
							console.log("done with clapping", data.data)
						

						},
						function error(err, status, config){
							console.log("We found the following errors")
							console.log(config)
							console.log(err.data)

						})
			});
			
		});
	}
}// end return
});


app.directive('likeDir', function($http){
	return {
		restrict: "EACM",
		link: function(scope, element, attrs){
			scope.$watch(attrs, function(){
				var token = (attrs.usertoken).replace(/['']/gi,"")
				var liked_by = (attrs.liker).replace(/[\s\s]/gi,"")
				console.log(liked_by)
				var postid = attrs.id
				console.log("This is for post like id", postid)
				scope.likes = attrs.count
				
				element.on('click', function(event){
					var config = {
						withCredentials: {'Authorization': token},
						'num_of_likes': parseInt(attrs.count) + 1,
						'liked_by': liked_by

					}

					$http.put("https://" + $location.$$host + "/like/change/"+ postid, config).then(function success(data, status, headers){
						scope.likes = data.data
						console.log(data.data)

					},
					function error(err, statusText, headers){
						console.log(err, err.statusText)
						if (err.statusText === "Unauthorized"){

							scope.alarm = true
							console.log("Alarm is on zo expect modal")
						}
					});
				})

			})
		}
	}
});

app.filter("NumFilter", function(){
	return function(num_to_change){
		var newValue = num_to_change;
    	if (num_to_change >= 1000) {
        	var suffixes = ["", "K", "M", "B","T"];
        	if ((""+num_to_change).length % 2 == 0){
        		var suffixNum = Math.floor( (""+num_to_change).length/4 );
        		console.log("suffix Num  as odd ", suffixNum)
        	}
        	else
        		var suffixNum = Math.floor( (""+num_to_change).length/3 );

        	var shortValue = '';
        	for (var precision = 2; precision >= 1; precision--) {
            	shortValue = parseFloat( (suffixNum != 0 ? (num_to_change / Math.pow(1000,suffixNum) ) : num_to_change).toPrecision(precision));
            	var dotLessShortValue = (shortValue + '').replace(/[^a-zA-Z 0-9]+/g,'');
            	if (dotLessShortValue.length <= 2) { break; }
        	}
        	if (shortValue % 1 != 0)  shortNum = shortValue.toFixed(1);
        	newValue = shortValue+suffixes[suffixNum];
    	}
    	return newValue;
	}

})

