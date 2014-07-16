# GradAgenda API Specification #

This document is to define communication protocol between GradAgenda frontend and GradAgenda backend.

## URL List ##

We will follow REST URL design pattern in URL design. For convenience, all HTTP method will be **POST**.

Some comments:

 - Since we have discussed that course data should be fetched "lazily", only when we fetch user's curriculum data, so maybe **UNINFO** module should be merged into curriculum module?

| URL | Function |
| :-: | :------: |
| /curriculum/fetch | Fetch user curriculum data to database |
| /curriculum/list  | Get the list of a user's courses in a semester |
| /curriculum/view   | Get the detail of a course |
| /curriculum/delete | Delete a course |
| /curriculum/update | Update a course |
| **[TODO] URL for other API need to be determined.** | |

## Protocol Specification ##

This chapter will show the request and return data format of each API. JSON will be our only data communication format.

### Common field ###

#### Request data ####

If you see [authentication required] in the following sections, which means the API will require front end to provide token(or other field) for authentication. Since our authentication strategy hasn't been fixed yet, we will leave the field name for later.

#### Return data ####

To handle error, every API will return two fields called "status" and "message". "status" contains a string telling front end whether the operation is success or not. Detail will be included into "message".

The format of "status" field:

| Status    | Explanation |
| :----:    | :-----: |
| "success" | operation completed |
| "error"   | an error occured |

The format of "message" field:

| Message | Status |
| :-----: | :----: |
| 'Unknown error.' | 'error' |
| **/curriculum/fetch** | |
| 'Fetching completed.' | 'success' |
| 'Error communicating with university servers.' | 'error' |
| 'Unknown university name.' | 'error' |
| 'Unknown semester.' | 'error' |
| 'Incorrect ID/password. Authentication failed.' | 'error' |
| 'Error authenticating with university servers. Please contact the developers.' | 'error' |
| **[TODO] message for other APIs need to be determined** | |

If the functionality of the API is requesting data from server, it will contain a field called "data". The format of each API is explained in the following section.

General return data structure will be:

```
{
    'status': STRING,
    'message': STRING,
    'data': JSON_OBJECT
}
```

### /curriculum/fetch ###

#### Request data format ####

```
{
    [authentication required]
    'university': STRING, // see below for avaiable value
    'username': STRING, // user name of school's curriculum system
    'password': STRING, // password of school's curriculum system
    'semester': STRING, // see below for available value
}
```

Available value of field 'university':

- 'UCBerkeley': University of California, Berkeley
- 'Purdue': Purdue University

Available value of field 'semester': [term]-[year]. [term] could be 'spring', 'summer', 'fall' or 'winter'. [year] could be '2014', '2013', .... For example, 'spring-2014'.

#### Return data format ####

no data returned.

### /curriculum/list ###

#### Request data format ####

```
{
    [authentication required]
    'user_id': STRING,
    'semester' : STRING,
}
```

#### Return data format ####

```
{
    lectures: [
        {
            'course_id': ID,
            'weedday': STRING,
            'starttime': DATETIME,
            'endtime': DATETIME,
            'location': STRING,
            'is_discussion': BOOLEAN
        }
    ]
}
```

### /curriculum/view ###
#### Request data format ####
```
{
    [authentication required]
    'course_id': ID
}
```
#### Return data format ####
```
{
    'name': STRING,
    'number': STRING,
    'college': STRING,
    'major': STRING,
    'grade': STRING,
    'professor': STRING,
    'description': STRING,
}
```
### /curriculum/delete ###
#### Request data format ####
```
{
    [authentication required]
    'course_id': ID
}
```
#### Return data format ####
no data returned.
### /curriculum/update ###
#### Request data format ####
```
{
    'course_id': ID,
    'name': STRING,
    'number': STRING,
    'college': STRING,
    'major': STRING,
    'grade': STRING,
    'professor': STRING,
    'description': STRING,
}
```
#### Return data format ####
no data returned.













