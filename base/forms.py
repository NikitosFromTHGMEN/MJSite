from django import forms


class SignInForm(forms.Form):
    login = forms.CharField(label="Логин:", widget=forms.TextInput(attrs={'class': "form-input"}))
    fname = forms.CharField(label="Имя:", widget=forms.TextInput(attrs={'class': "form-input"}))
    lname = forms.CharField(label="Фамилия:", widget=forms.TextInput(attrs={'class': "form-input"}))
    date_of_birth = forms.DateField(label="Дата рождения:", widget=forms.DateInput(attrs={'type': 'date', 'class': "form-input"}))
    email = forms.EmailField(label="email:", widget=forms.TextInput(attrs={'class': "form-input"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-input"}), label="Пароль:")
    password_conf = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-input"}),
                                    label="Подтвердите пароль:")
