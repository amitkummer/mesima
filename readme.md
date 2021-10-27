# DRF Useful Links

- A solution to the wierd API endpoinds in the form of `user/id/tasks` ([link](https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#refactoring-to-use-viewsets)).

- Writing 'raw' gin-like views in DRF ([link](https://www.django-rest-framework.org/tutorial/1-serialization/#writing-regular-django-views-using-our-serializer)).

- Overwrite just the post in the viewset which is prob the best move ([link](https://www.django-rest-framework.org/tutorial/quickstart/)).



# Notes

- `Post` returns data in headers. :(
- `People` email field should be unique.


# Questions to Lecturer

1. Can we return error messages in `JSON`? (There is a fix though (link)[https://www.django-rest-framework.org/api-guide/settings/#miscellaneous-settings]).


# TODO

1. The weird nested endpoints (like `/tasks/id/owner`).
2. Complete `Person`'s `activeTaskCount`.
