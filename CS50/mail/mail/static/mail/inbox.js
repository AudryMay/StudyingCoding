document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', send_email);
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email =>{
      const element = document.createElement('div');
      element.className = 'card'
      element.className = email.read ? 'read' : 'unread';
      element.innerHTML = `
      <div class="card-body">
      <div class="d-flex align-items-baseline">
      <h6 class='card-title w-50'>${email.sender}</h6>
      <h8 class="card-subtitle text-muted text-right w-50">${email.timestamp}</h8>
      </div>
      <h7 class='card-body'>${email.subject}</h7>
      </div>
      `;
      element.addEventListener('click', () => view_email(mailbox, email.id));
      document.querySelector('#emails-view').append(element);
    
      
  })
  });
}

function send_email()
{
  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value;
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients:recipients,
      subject:subject,
      body:body
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
    load_mailbox("sent");
  });
}


function view_email(mailbox, id)
{
  console.log("Clicked!");
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email =>{
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#single-email-view').style.display = 'block';

      document.querySelector('#single-email-view').innerHTML = ''

      const element = document.createElement('div');
      element.innerHTML=`
      <div class="card">
        <div class='card-body'>
          <ul class='list-group-flush'>
            <li class='list-group-item'><h7><strong>From: </strong>${email.sender}</h7></li>
            <li class='list-group-item'><h7><strong>To: </strong>${email.recipients}</h7></li>
            <li class='list-group-item'><h7><strong>Subject: </strong>${email.subject}</h7></li>
            <li class='list-group-item mt-2'><p>${email.body}</p></li>
          </ul>
        </div>
      </div>
      `
      document.querySelector('#single-email-view').append(element);
      
      if(!email.read)
      {
        console.log("sending read");
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        });
      }
      
      
      const archive = document.createElement('button');
      archive.className = email.archived? 'btn btn-danger' : 'btn btn-success';
      archive.innerHTML = email.archived? 'Unarchive':'Archive';
      archive.addEventListener('click', () => {
        console.log("sending archive");
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
        }).then(()=>{load_mailbox("inbox");});
      });
      document.querySelector('#single-email-view').append(archive);
      
      if(mailbox === 'inbox')
      {
        const reply = document.createElement('button');
        reply.className = 'btn btn-primary';
        reply.innerHTML = 'Reply';
        reply.addEventListener('click', () => {
          recipients = email.sender;
          let re = email.subject.indexOf("Re: ");
          subject = re == -1 ? "Re: " + email.subject : email.subject;
          compose_email();
          document.querySelector('#compose-recipients').value = recipients;
          document.querySelector('#compose-subject').value = subject;
          document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n ${email.body}`;
        });
        document.querySelector('#single-email-view').append(reply);
  }

  });
}