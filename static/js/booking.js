document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[data-borrowed-from-id]').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();
            const userId = this.getAttribute('data-borrowed-from-id');
            fetchUserDetails(userId);
        });
    });
    document.querySelectorAll('a[data-lent-to-id]').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();
            const userId = this.getAttribute('data-lent-to-id');
            fetchUserDetails(userId);
        });
    });

});

function fetchUserDetails(userId) {
    fetch(`/user/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                populateUserDetailsModal(data);
                $('#userDetailsModal').modal('show');
            }
        })
        .catch(error => console.error('Error fetching user details:', error));
}

function populateUserDetailsModal(user) {
    const userDetailsTable = document.getElementById('userDetailsTable');
    userDetailsTable.innerHTML = `
        <tr><th>Name</th><td>${user.name}</td></tr>
        <tr><th>Phone Number</th><td>${user.phone_number}</td></tr>
        <tr><th>Email</th><td>${user.email}</td></tr>
        <tr><th>Village</th><td>${user.village_name}</td></tr>
        <tr><th>Sub District</th><td>${user.sub_district_name}</td></tr>
    `;
}

function openEditModal(bookingId, isStarted, isCompleted) {
    $('#editModal').modal('show');
    isStarted = (isStarted === 'True');
    isCompleted = (isCompleted === 'True');

    const bookingCompletedMessage = document.getElementById('bookingCompletedMessage');
    if (!isStarted) {
        console.log('booking not started');
        bookingCompletedMessage.style.display = 'none';
        document.getElementById('completeBooking').disabled = true;
        document.getElementById('startBooking').disabled = false;
        document.getElementById('startBooking').onclick = () => {
            fetch(`/updateBooking/${bookingId}?action=start`, {
                method: 'POST'
            })
            .then(response => response.text())
            .then(data => {
                alert('Booking started successfully!');
                $('#editModal').modal('hide');
                location.reload();
            })
            .catch(error => console.error('Error:', error));
        };
    } else if (!isCompleted) {
        bookingCompletedMessage.style.display = 'none';
        document.getElementById('startBooking').disabled = true;
        document.getElementById('completeBooking').disabled = false;
        document.getElementById('completeBooking').onclick = () => {
            fetch(`/updateBooking/${bookingId}?action=complete`, {
                method: 'POST'
            })
            .then(response => response.text())
            .then(data => {
                alert('Booking completed successfully!');
                $('#editModal').modal('hide');
                location.reload();
            })
            .catch(error => console.error('Error:', error));
        };
    } else {
        document.getElementById('startBooking').disabled = true;
        document.getElementById('completeBooking').disabled = true;
        bookingCompletedMessage.style.display = 'block';
    }
}