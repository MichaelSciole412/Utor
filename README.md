# Utor
Utor is a web based service for connecting people in college who need tutors and study groups.

Utor is a web application written in python using the Django framework (no not Jamie Foxx) and uses a Sqlite database.

## Goals
Utor has two main aims:
- To connect students to tutors who are the best match for them
- To help organize study groups for students who share studies

## Features
- Utor creates a list of tutors for students to view based off of the tutors':
  - areas of expertise
  - ratings from other students
  - university affiliation
  - location
  - payment rates
- Using a ZIP code API, the distance between students and tutors is determined and tutors are ordered by their distance to the student--only tutors within 5 miles are shown.
- Direct messaging feature for allowing students to connect to potential tutors and exchange contact information, plan sessions, etc.

- Utor also allows students to post study group listings to their respective universities.
  - Students from the same university can opt in for a study group, so long as they are approved by the admin.
  - Students acting as admins for the study group can set times and locations for meetings. 
  - Only members of the group can view meeting details, otherwise details are hidden. 
  - Members can post helpful information regarding the subject matter, meeting organization, and important dates!
	- Members can comment on posts
  - Students can engage with other students in a live group chat to help each other with course material, plan meetings, etc.

## Timeline (3/26/2024 - End)
- 3/26 - 4/2
  - Ben will complete scheduling meetings for study groups
  - Michael will complete Reviews for study groups
- 4/2 - 4/9
  - Michael will complete instant messaging functionality
  - Ben will complete the homepage displaying basic website information and the 404 page
- 4/9 - 4/16
  - Michael and Ben will complete finishing touches involving front-end aspects of the website like CSS as well as bug testing.
- 4/16 - End
  - Michael and Ben will get help to host the website on the student2 server.  After hosting the website, we will continue bug testing and bug fixes.
