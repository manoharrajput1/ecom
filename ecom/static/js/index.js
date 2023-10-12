
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