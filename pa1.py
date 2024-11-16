# Name: pa1.py
# Author(s): Olivia Kallmeyer and Tia Merheb
# Date: Feb 11, 2023
# Description: Gale Shapley

import queue as Queue

def gale_shapley(filename):
    """
    Runs Gale-Shapley algorithm on input
    from file filename.  Format of input file
    given in problem statement.
    Returns a list containing hospitals assigned to each 
    student, or None if a student is not assigned to a hospital.
    """

    with open(filename, 'r') as f:
        num_hospitals, num_students = map(int, f.readline().strip().split())

        # initialize hospital and student preferences in dictionaries
        student_prefs = {}
        hospital_prefs = {}
        student_rankings = {}

        # read number of positions available for each hospital
        num_positions = {}
        hospital_slots = [int(slots) for slots in f.readline().split()]

        # read the hospital preferences
        for h in range(num_hospitals):
            line = list(map(int, f.readline().strip().split()))
            hospital_prefs[h] = line

        # Read the student preferences
        for s in range(num_students):
            line = list(map(int, f.readline().strip().split()))
            student_prefs[s] = line
            rankings = [-1] * num_hospitals
            for i in range(num_hospitals):
                rankings[line[i]] = i
            student_rankings[s] = rankings

        # Add hospitals to a queue
        proposingHospitals = Queue.Queue()
        for i in range(num_hospitals):
            proposingHospitals.put(i)   

        # Initialize the matchings
        hospital_matchings = {}
        num_proposals = [0] * num_hospitals

        # While loop runs as long as there are hospitals that still need to propose
        while not proposingHospitals.empty():
            h = proposingHospitals.get()
            hospital_preferences = hospital_prefs[h]
            curr_preference = num_proposals[h]

            if hospital_slots[h] > 0 and curr_preference < len(hospital_preferences):
                s = hospital_preferences[curr_preference]

                if s not in hospital_matchings:
                    # Case 1: hospital has no matches yet
                    if hospital_slots[h] > 0:
                        hospital_matchings[s] = h
                        hospital_slots[h] -= 1
                else:
                    # Case 2: hospital already has a match
                    curr_match = hospital_matchings[s]
                    curr_match_ranking = student_rankings[s][curr_match]
                    proposed_match_ranking = student_rankings[s][h]

                    if proposed_match_ranking < curr_match_ranking:
                        # Proposed hospital is more preferable, so match it with this student
                        hospital_matchings[s] = h
                        hospital_slots[h] -= 1
                        hospital_slots[curr_match] += 1
                        proposingHospitals.put(curr_match)
                    else:
                        # Current match is more preferable, so keep it
                        proposingHospitals.put(h)

                num_proposals[h] += 1

                if hospital_slots[h] > 0 and curr_preference < len(hospital_preferences) - 1:
                    proposingHospitals.put(h)

        # Output a list where indices are students and element is the hospital they are matched to
        assignments = [hospital_matchings.pop(s, None) for s in range(num_students)]
        return assignments