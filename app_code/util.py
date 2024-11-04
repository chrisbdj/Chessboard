def arrays_equal(A, B):
    # If lengths of array are not equal means array are not equal
    if len(A) != len(B):
        return False
    
    #Simple test if all values ate the same
    if A == B:
        return True
    else: #they are not the same
        return False




def whats_the_dif(old, new):
    differences = []
    for i in range(len(new)):
        if old[i] != new[i]:
            differences.append({"index": i, "state": new[i]})
            
    return differences


def count_states(arr, checkFor):
    count = 0
    for states in arr:
        if states["state"] == checkFor:
            count += 1
    return count
            

def split_string(string, length):
    return [string[i:i+length] for i in range(0, len(string), length)]





