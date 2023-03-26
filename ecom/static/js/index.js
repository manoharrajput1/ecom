var updateBtns = document.getElementsByClassName('update-cart')
var viewBtn = document.getElementsByClassName('viewbtn')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function () {
		var productId = this.dataset.product
		var action = this.dataset.action
		updateUserOrder(productId, action)
	})
}
for (i = 0; i < viewBtn.length; i++) {
	viewBtn[i].addEventListener('click', function () {
		var productId = this.dataset.product
		viewData(productId)
	})
}

function updateUserOrder(productId, action) {
	var url = '/update_item/'
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({ 'productId': productId, 'action': action })
	})
	.then((response) => {
		return response.json();
	})
	.then((data) => {
		console.log('hello');
		location.reload()
	})
}
function viewData(productId) {
	var url = '/viewpred/'
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({ 'productId': productId})	
	})
	.then((response) => {
		return response.json();
		console.log(productId);
	})
	.then((data) => {
		console.log('hello');
	})
}
