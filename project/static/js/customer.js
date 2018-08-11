var app = angular.module('refearn', []);
app.controller('refearnController', function($scope, $http){
    $scope.addReferral = function(){
        $http.put('/api/customer/'+$scope.customer+'/?referrer='+$scope.referrer)
    }
    $scope.addAmbassodor = function(){
        var doj = new Date($scope.joining_date)
        doc = doj.getFullYear()+"-"+(doj.getMonth()+1)+"-"+doj.getDate()
        var data = {email: $scope.email, joining_date:doc, referral_id:$scope.referral_id, is_ambassador:true}
        $http.post('/api/customer/', data)

    }
})