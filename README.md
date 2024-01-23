# Utor
Utor is a web based service for connecting people in college who need tutors and study groups.

Utor is a web application written in python using the Django framework (no not Jamie Foxx) and uses a MySql database.

## Goals
Utor has two main aims:
- To connect students to tutors who are the best match for them
- To help organize study groups for students who share studies

## Features
- Utor creates a list of tutors for students to view based off of the tutors':
  - areas of expertise
  - credentials
  - ratings from other students
  - university affiliation
  - location
  - payment rates

- Utor also allows students to post study group listings to their respective universities.
  - Students from the same university can opt in for a study group, so long as they are approved by the admin, and the group is not full.
  - Students acting as admins for the study group can set times and locations for meetings. 
  - Only members of the group can view meeting details, otherwise details are hidden. 
  - Members can post helpful information regarding the subject matter, meeting organization, and important dates!
	- Members can comment on posts, ideally to help organize a meeting schedule

## Extended Features
- Use google maps API to determine the distance between students and tutors and show students the tutors closest to them first
- Direct messaging feature for allowing students to connect to potential tutors and exchange contact information, plan sessions, etc.
- File hosting for study groups